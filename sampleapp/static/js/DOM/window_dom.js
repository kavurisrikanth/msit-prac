﻿function win_dom(){var e,u,h,t,i,a,v,form_sub;var o=$("win"),n,f=document.createElement("div");f.id="rec_bkg",n=document.createElement("span"),n.id="rec_bkg_title",i=document.createTextNode("Recorder"),n.appendChild(i),f.appendChild(n),o.appendChild(f),e=document.createElement("span"),e.id="sheet_tb1",u=document.createElement("input");u.id="sheet_play";u.type="button";u.setAttribute('class','mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent');u.value="►";u.setAttribute("onclick","piano.recplay()");e.appendChild(u);t=document.createElement("span");t.id="sheet_stop_sep";t.className="sep";i=document.createTextNode(" | ");t.appendChild(i);e.appendChild(t);u=document.createElement("input");u.id="sheet_stop";u.type="button";u.setAttribute('class','mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent');u.value="■";u.setAttribute("onclick","win_fnc.stop()");e.appendChild(u);o.appendChild(e);h=document.createElement("input");h.id="recplay";h.type="button";h.setAttribute('class','mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent');h.value="●";h.setAttribute("onclick","piano.recplay(true)");e.appendChild(h);a=document.createElement("textarea");a.className="rec_txt";a.placeholder="Sheet";a.id="s1";o.appendChild(a);n=document.createElement("input");n.id='chat-message-submit';n.type="submit";n.setAttribute('class','mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent');n.value="Send";e.appendChild(n);win_fnc.viewer()}
if(!hideRecorder){win_dom()}
piano.assist()