/*1366606543,178142559*/

if (self.CavalryLogger) { CavalryLogger.start_js(["qu1rX"]); }

__d("MusicDiagnostics",["Arbiter","copyProperties","MusicConstants"],function(a,b,c,d,e,f){var g=b('Arbiter'),h=b('copyProperties'),i=b('MusicConstants');function j(l,m){return {time:new Date(),data:m,provider:l};}var k={sendUpdate:function(l,m,n){g.inform('MusicDiagnostics/send',h(j(l,n),{op:m}));},receiveUpdate:function(l,m){g.inform('MusicDiagnostics/receive',h(j(l,m),{op:i.STATUS_CHANGE_OP.STATUS}));},stateChanged:function(l,m,n,o){g.inform('MusicDiagnostics/state_change',h(j(l,o),{from:m,to:n}));},userAction:function(l,m,n){g.inform('MusicDiagnostics/user_action',h(j(l,n),{action:m}));},debug:function(l,m,n){g.inform('MusicDiagnostics/debug',h(j(l,n),{str:m}));},WINDOW_OPEN:'window_open',ATTEMPTING_LAUNCH:'launching',INSTALL_STARTED:'install_started',PLAY_SONG:'play_song',LAUNCH_NOT_NEEDED:'launch_not_needed',LAUNCH_CLICK_CANCEL:'launch_click_cancel',INSTALL_CLICK_CANCEL:'install_click_cancel',SWITCHED_PROVIDER:'switched_provider',TOS_SHOWN:'tos_shown',TOS_CLICK_CANCEL:'tos_click_cancel'};e.exports=a.MusicDiagnostics||k;});