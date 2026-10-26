// Le nom s'affiche une fois inspecté comme dans les DevTools, puis l'inspection
// revient au survol ou au focus.
const inspect = document.getElementById('inspect');
const dims = document.getElementById('dims');

function showDims() {
  const box = inspect.querySelector('h1').getBoundingClientRect();
  dims.textContent = `${Math.round(box.width)} × ${Math.round(box.height)}`;
}

function setInspect(on) {
  if (on) showDims();
  inspect.classList.toggle('on', on);
}

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduceMotion) {
  setTimeout(() => setInspect(true), 400);
  setTimeout(() => setInspect(false), 3200);
}
inspect.addEventListener('mouseenter', () => setInspect(true));
inspect.addEventListener('mouseleave', () => setInspect(false));

// Veille : les données viennent de data/veille.json, mis à jour par GitHub Actions.
function item(name, detail, href) {
  const li = document.createElement('li');
  const title = document.createElement(href ? 'a' : 'span');
  title.className = 'name';
  title.textContent = name;
  if (href) title.href = href;
  const small = document.createElement('span');
  small.className = 'detail';
  small.textContent = detail;
  li.append(title, small);
  return li;
}

function fill(list, items) {
  list.replaceChildren(...items);
  if (!items.length) {
    const li = document.createElement('li');
    li.className = 'empty';
    li.textContent = 'Rien de nouveau pour le moment.';
    list.append(li);
  }
}

fetch('data/veille.json', { cache: 'no-cache' })
  .then((res) => res.json())
  .then((data) => {
    fill(document.getElementById('leaks'),
      data.leaks.map((l) => item(l.source, l.date)));
    fill(document.getElementById('repos'),
      data.repos.map((r) => item(r.name, r.description, r.url)));
    if (data.updated) {
      const date = new Date(data.updated).toLocaleString('fr-FR', {
        day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit',
      });
      document.getElementById('veille-maj').textContent =
        `Mise à jour automatique toutes les six heures. Dernière mise à jour : ${date}.`;
    }
  })
  .catch(() => {
    for (const id of ['leaks', 'repos']) {
      document.getElementById(id).innerHTML =
        '<li class="empty">La veille n\'a pas pu être chargée. Rechargez la page.</li>';
    }
  });
