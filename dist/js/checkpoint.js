// Shared validation for both disk checkpoints and imported files.
export function validateCheckpoint(s, size=128){
 const fail=message=>{throw new Error(message);};
 if(!s||s.version!==1||s.size!==size||!['glider','garden','collide','soup'].includes(s.preset)||!Number.isSafeInteger(s.tick)||s.tick<0||!Number.isFinite(s.baseline)||s.baseline<=0||!Number.isSafeInteger(s.seed)||typeof s.auto!=='boolean')fail('Unsupported world file.');
 const arrays={};for(const k of ['s0','s1']){const a=s[k];if(!(Array.isArray(a)||a instanceof Float32Array)||a.length!==size*size*4||!a.every(v=>Number.isFinite(v)&&v>=0&&v<=1e6))fail('Invalid world state.');arrays[k]=Float32Array.from(a);}
 const ranges={dt:[.01,.2],speed:[1,6],radius:[13,13],predPayoff:[0,1],mu:[.05,.4],sigma:[.001,.1],mut:[0,.015],light:[0,1],time:[0,1e12],curiosity:[0,0],massScale:[.9,1.1],pokeR:[0,.1],pokeAmt:[0,1]};const params={};
 for(const[k,[lo,hi]]of Object.entries(ranges)){const v=s.params?.[k];if(!Number.isFinite(v)||v<lo||v>hi)fail('Invalid environment settings.');params[k]=v;}
 if(![1,3,6].includes(params.speed))fail('Invalid speed.');for(const k of ['massConserve','genome','metabolism','eat','pokeErase']){if(typeof s.params[k]!=='boolean')fail('Invalid environment toggle.');params[k]=s.params[k];}params.poke=[-1,-1];
 if(!Array.isArray(s.entries)||s.entries.length>80||s.entries.some(e=>!Number.isSafeInteger(e.tick)||e.tick<0||typeof e.text!=='string'||e.text.length>300))fail('Invalid journal.');
 const c=s.caretaker;if(!c||!Number.isSafeInteger(c.updates)||c.updates<0||!c.q||Array.isArray(c.q)||typeof c.q!=='object'||Object.entries(c.q).some(([k,v])=>! /^[0-2]:[0-2]$/.test(k)||!Array.isArray(v)||v.length!==4||v.some(x=>!Number.isFinite(x)||Math.abs(x)>100)))fail('Invalid caretaker memory.');
 if(c.rngState!==undefined&&(!Number.isInteger(c.rngState)||c.rngState<0||c.rngState>4294967295))fail('Invalid random state.');
 if(c.last!=null&&(!/^[0-2]:[0-2]$/.test(c.last.state)||!Number.isInteger(c.last.action)||c.last.action<0||c.last.action>3||!Number.isFinite(c.last.mass)||c.last.mass<0))fail('Invalid caretaker transition.');
 return{version:1,size,...arrays,params,tick:s.tick,seed:s.seed,preset:s.preset,baseline:s.baseline,entries:s.entries.map(e=>({tick:e.tick,text:e.text})),caretaker:{q:Object.fromEntries(Object.entries(c.q).map(([k,v])=>[k,v.slice()])),updates:c.updates,rngState:c.rngState,last:c.last?{...c.last}:null},auto:params.genome&&s.auto,savedAt:typeof s.savedAt==='string'&&!Number.isNaN(Date.parse(s.savedAt))?s.savedAt:new Date().toISOString(),lastDecision:Number.isSafeInteger(s.lastDecision)&&s.lastDecision>=0&&s.lastDecision<=s.tick?s.lastDecision:s.tick,lastJournal:Number.isSafeInteger(s.lastJournal)&&s.lastJournal>=0&&s.lastJournal<=s.tick?s.lastJournal:s.tick};
}
