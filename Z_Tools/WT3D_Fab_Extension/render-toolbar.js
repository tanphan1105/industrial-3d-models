// Detect Fab's actual painted pill bar, not a fraction of the whole viewport.
// English toolbar proportions measured from the native Fab editor (2026-10-22).
((root, factory) => {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.WT3DToolbar = api;
})(typeof globalThis === 'object' ? globalThis : this, () => {
  'use strict';
  const centers = {scene:.051, lighting:.166, materials:.286, camera:.410, look:.518,
    annotations:.649, animation:.783, inspect:.906};
  function detect({data, width, height}) {
    const rows = [];
    const blue = i => data[i] < 100 && data[i+1] > 110 && data[i+2] > 150;
    const barPixel = (x,y) => {const i=(y*width+x)*4; return data[i+3]>200 &&
      ((data[i]<45 && data[i+1]<45 && data[i+2]<45) || blue(i));};
    for (let y=Math.max(0,height-60);y<height-3;y++) {
      let start=-1, last=-1, gaps=0;
      const flush = () => {
        const w=last-start+1;
        if(start>=0 && w>width*.18 && w<width*.80 && Math.abs((start+last)/2-width/2)<width*.025) rows.push({x:start,y,width:w});
        start=-1;last=-1;gaps=0;
      };
      for(let x=0;x<width;x++) {
        if(barPixel(x,y)){if(start<0)start=x;last=x;gaps=0;}
        else if(start>=0 && ++gaps>3)flush();
      }
      flush();
    }
    if(rows.length<5) throw new Error('Không nhận diện được thanh tab Fab trong ảnh canvas; không click đoán.');
    rows.sort((a,b)=>b.width-a.width);
    const best=rows.filter(r=>r.width>=rows[0].width*.95);
    best.sort((a,b)=>a.y-b.y);
    const middle=best[Math.floor(best.length/2)];
    // Use the vertical median of the full-width band, not its upper/lower border.
    return {x:middle.x,y:(best[0].y+best[best.length-1].y)/2,width:middle.width};
  }
  function point(bar,name) {
    if(!(name in centers)) throw new Error('Unsupported Fab tab');
    return {x:bar.x+bar.width*centers[name],y:bar.y};
  }
  function active(img,bar,name) {
    const p=point(bar,name);let yes=0,total=0;
    const radius = Math.max(12, Math.round(bar.width * .036));
    for(let y=Math.round(p.y)-4;y<=Math.round(p.y)+4;y++) for(let x=Math.round(p.x)-radius;x<=Math.round(p.x)+radius;x++) {
      if(x<0||y<0||x>=img.width||y>=img.height)continue;
      const i=(y*img.width+x)*4;total++;
      if(img.data[i]<100&&img.data[i+1]>110&&img.data[i+2]>150)yes++;
    }
    return total>0 && yes/total>.28;
  }
  async function capture(canvas) {
    await new Promise(requestAnimationFrame);
    const copy=document.createElement('canvas');copy.width=canvas.width;copy.height=canvas.height;
    const ctx=copy.getContext('2d',{willReadFrequently:true});ctx.drawImage(canvas,0,0);
    return ctx.getImageData(0,0,copy.width,copy.height);
  }
  return {detect,point,active,capture};
});
