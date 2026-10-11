(function(){var c=document.getElementById('fx');if(!c||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
var x=c.getContext('2d'),P=[],W,H,N=42;function rs(){W=c.width=c.offsetWidth;H=c.height=c.offsetHeight}rs();addEventListener('resize',rs);
for(var i=0;i<N;i++)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35});
(function f(){x.clearRect(0,0,W,H);P.forEach(function(p,i){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
x.fillStyle='rgba(34,211,238,.8)';x.fillRect(p.x,p.y,2,2);for(var j=i+1;j<N;j++){var q=P[j],d=Math.hypot(p.x-q.x,p.y-q.y);
if(d<120){x.strokeStyle='rgba(139,92,246,'+(1-d/120)*.3+')';x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);x.stroke()}}});requestAnimationFrame(f)})()})();