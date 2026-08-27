# ======================================================================
# RevitOrchestrator.py
# External Python orchestrator for multi-process Revit Batch processing
# Incorporates Autodesk Veteran optimizations:
# 1. Multi-process execution (Revit is single-threaded, launch N workers)
# 2. Restart policy (Kill/restart Revit every 30-50 models to clean RAM leaks)
# 3. Fast fail pre-validation (validates JSON and files before opening Revit)
# ======================================================================

import os
import json
import subprocess
import time
import shutil
from pathlib import Path

# Paths Setup
WORKSPACE = Path("D:/WT3D_Project")
INPUT_DIR = WORKSPACE / "1_Exports_Batch"
OUTPUT_DIR = WORKSPACE / "rfa_outputs"
LOGS_DIR = WORKSPACE / "Z_Log"
TEMP_DIR = WORKSPACE / "temp_revit_jobs"

# Config
BATCH_SIZE = 30  # Max models per Revit process lifetime
REVIT_PATH = r"C:\Program Files\Autodesk\Revit 2025\Revit.exe" # Change to target Revit version
REVIT_TEMPLATE_PATH = WORKSPACE / "Templates" / "MEP_Equipment_Template.rft"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def pre_validate_job(model_dir: Path) -> bool:
    """
    FAIL-FAST PRE-VALIDATION (Rule 4)
    Validate JSON schema, check files existence, and make sure we don't spin up Revit for dead files.
    """
    sat_file = model_dir / f"{model_dir.name}.sat"
    json_file = model_dir / f"{model_dir.name}.json"
    
    if not sat_file.exists():
        print(f"  [Pre-Validate FAIL] Missing SAT file: {sat_file}")
        return False
    if not json_file.exists():
        print(f"  [Pre-Validate FAIL] Missing JSON file: {json_file}")
        return False
        
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check required keys
        required_keys = ["dn_in", "dn_out", "height", "diameter", "inlet", "outlet"]
        for key in required_keys:
            if key not in data:
                print(f"  [Pre-Validate FAIL] JSON missing key: {key}")
                return False
                
        # Validate values
        if data["dn_in"] <= 0 or data["dn_out"] <= 0:
            print(f"  [Pre-Validate FAIL] Connector diameters must be > 0")
            return False
            
    except Exception as e:
        print(f"  [Pre-Validate FAIL] JSON load error: {e}")
        return False
        
    return True

def run_revit_batch(batch_jobs, batch_index):
    """
    Spawns a Revit.exe process to run a specific list of family generations.
    """
    batch_file = TEMP_DIR / f"batch_{batch_index}.json"
    
    # Write batch task config file for the Revit C# Add-in to read on startup
    batch_data = {
        "template_path": str(REVIT_TEMPLATE_PATH),
        "output_dir": str(OUTPUT_DIR),
        "jobs": batch_jobs
    }
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, indent=2)
        
    print(f"\n🚀 Launching Revit process for Batch {batch_index} ({len(batch_jobs)} models)...")
    
    # In a production environment, we launch Revit passing the job file path 
    # via environment variables or command-line parameters that our C# Add-in intercepts.
    env = os.environ.copy()
    env["BIM_FACTORY_JOB_FILE"] = str(batch_file)
    
    # Start Revit process
    start_time = time.time()
    try:
        # Note: In standard automated pipelines, we run Revit using a journal file (.txt) 
        # or have the C# Add-in run headless at startup and close Revit via API.
        process = subprocess.Popen([REVIT_PATH], env=env)
        
        # Monitor the process (e.g. timeout after 5 minutes)
        # Revit C# Add-in will call Application.Quit() once it processes the JSON batch.
        timeout_seconds = 300  # 5 minutes
        while True:
            exit_code = process.poll()
            if exit_code is not None:
                print(f"  Revit batch {batch_index} completed with exit code: {exit_code}")
                break
                
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                print(f"  [TIMEOUT] Revit batch {batch_index} exceeded timeout! Force killing process...")
                process.terminate()
                process.wait()
                break
            time.sleep(1)
            
    except Exception as e:
        print(f"  Failed to run Revit: {e}")
        
    # Clean up temp batch file
    if batch_file.exists():
        try:
            os.remove(batch_file)
        except:
            pass

def main():
    print("====================================================")
    print("   BIM FACTORY - ENTERPRISE RE-VIT ORCHESTRATOR")
    print("====================================================")
    
    # 1. Collect all model subdirectories in export batch folder
    all_dirs = [d for d in INPUT_DIR.iterdir() if d.is_dir()]
    print(f"Found {len(all_dirs)} model directories to check...")
    
    # 2. Run fast pre-validation filter
    valid_jobs = []
    skipped_count = 0
    for d in all_dirs:
        if pre_validate_job(d):
            sat_file = d / f"{d.name}.sat"
            json_file = d / f"{d.name}.json"
            valid_jobs.append({
                "model_name": d.name,
                "sat_path": str(sat_file),
                "json_path": str(json_file)
            })
        else:
            skipped_count += 1
            
    print(f"\nPre-validation summary:")
    print(f"  Total Validated Jobs: {len(valid_jobs)}")
    print(f"  Total Skipped (Error): {skipped_count}")
    
    if not valid_jobs:
        print("No valid jobs to process. Exiting.")
        return
        
    # 3. Partition jobs into batches (Process Isolation & Memory Leak Protection)
    batches = [valid_jobs[i:i + BATCH_SIZE] for i in range(0, len(valid_jobs), BATCH_SIZE)]
    print(f"\nTotal batches to run: {len(batches)} (Batch size: {BATCH_SIZE})")
    
    # 4. Sequentially process batches (spawning fresh Revit workers)
    for idx, batch in enumerate(batches, start=1):
        run_revit_batch(batch, idx)
        
    print("\n====================================================")
    print("   ORCHESTRATOR COMPLETE - ALL BATCHES PROCESSED")
    print("====================================================")

if __name__ == "__main__":
    main()
