/* 名刺のQRコード（https://exhoumu.github.io/index.html#contact）から来た人には、まずトップ（どんな事務所か・代表の紹介）を見せる。
   見分け方：アドレスが index.html#contact で、前のページの記録（referrer）がないとき。サイト内のボタンから来た人は今までどおりお問い合わせ欄へ。 */
(function(){try{
 if(location.hash==='#contact'&&/\/index\.html$/.test(location.pathname)&&!document.referrer){
  history.replaceState(null,'',location.pathname.replace(/index\.html$/,''));
  try{history.scrollRestoration='manual'}catch(e){}
  var top=function(){window.scrollTo({top:0,left:0,behavior:'instant'})};top();
  window.addEventListener('DOMContentLoaded',top);window.addEventListener('load',function(){setTimeout(top,0);setTimeout(top,300);setTimeout(top,800)});
 }}catch(e){}})();
