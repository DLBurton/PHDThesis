/*!CK:2666605793!*//*1386599213,173213749*/

if (self.CavalryLogger) { CavalryLogger.start_js(["2xA31"]); }

__d("MusicLogger",["AsyncRequest","JSLogger","MusicConstants","Run","setTimeoutAcrossTransitions"],function(a,b,c,d,e,f){var g=b('AsyncRequest'),h=b('JSLogger'),i=b('MusicConstants'),j=b('Run'),k=b('setTimeoutAcrossTransitions'),l=5000,m=h.create('music_logger'),n=null,o={};function p(){n=null;}function q(){if(!n){m.debug('queue_dispatch',l);n=k(r,l);}}function r(t){m.debug('dispatch',{onUnload:t,messages:o});p();if(Object.keys(o).length>0){var u=JSON.stringify(o);o={};var v=new g().setURI('/ajax/music/log.php').setData({types:u});if(t)v.setOption('asynchronous',false);v.send();}}j.onUnload(r.bind(null,true));var s={PLATFORM:'platform',STATUS_EVENT_VIA:'status_event',BUMP_KEY:'bump_key',log:function(t,u){if(t===s.STATUS_EVENT_VIA)if(u.op!==i.OP.PLAY&&u.op!==i.STATUS_CHANGE_EVENT.playing&&u.op!==i.STATUS_CHANGE_EVENT.track)return;o[t]=o[t]||[];o[t].push(u);q();},dispatchNow:r};e.exports=a.MusicLogger||s;});
__d("legacy:Music",["Music"],function(a,b,c,d){a.Music=b('Music');},3);