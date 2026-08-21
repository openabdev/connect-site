// Send a first-time visitor to their own language, then remember the choice.
//
// Cloned in behaviour from foldic.app rather than re-derived: ?lang= wins, then a
// stored choice, then navigator.languages. English returns early so an
// English-preferring visitor is never redirected away from the page they asked for.
(function () {
  var KEY = "openab-connect-lang";
  var here = document.documentElement.getAttribute("data-lang") || "en";
  var base = document.documentElement.getAttribute("data-base") || "/";
  var params = new URLSearchParams(location.search);

  // An explicit ?lang= is a decision: record it and do not redirect.
  var asked = params.get("lang");
  if (asked) {
    try { localStorage.setItem(KEY, asked === "en" ? "/" : "/" + asked + "/"); } catch (e) {}
    return;
  }
  // Only the canonical English page redirects; a visitor already on /zh/ has
  // arrived somewhere deliberate.
  if (here !== "en") {
    try { localStorage.setItem(KEY, base); } catch (e) {}
    return;
  }

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved) {
    if (saved !== "/") location.replace(saved + location.hash);
    return;
  }

  var map = [[/^zh/i, "/zh/"], [/^ja/i, "/ja/"], [/^ko/i, "/ko/"]];
  var langs = navigator.languages && navigator.languages.length
    ? navigator.languages : [navigator.language || ""];
  for (var i = 0; i < langs.length; i++) {
    for (var j = 0; j < map.length; j++) {
      if (map[j][0].test(langs[i])) { location.replace(map[j][1] + location.hash); return; }
    }
    if (/^en/i.test(langs[i])) return;  // English preferred before any match
  }
})();
