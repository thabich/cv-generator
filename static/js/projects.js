const skills = JSON.parse(document.getElementById('skills-json').textContent);
const container = document.getElementById('projects-container');

function renderProject(project) {
  const div = document.createElement('div');
  div.className = 'project';
  div.dataset.projectId = project.id;

  div.innerHTML = `
    <h3>${project.name}</h3>
    <div class="skill-picker"></div>
    <button onclick="editProject(${project.id})">Edit</button>
  `;

  container.appendChild(div);

  // SkillPicker initialisieren
  new SkillPicker(div.querySelector('.skill-picker'), skills, project.skills || []);
}

function editProject(id) {
  const project = existingTasks.find(p => p.id === id);
  if (!project) return alert('Projekt nicht gefunden');
  // hier könntest du Edit-Modal öffnen
  console.log('Edit Project', project);
}

function renderAllProjects() {
  container.innerHTML = '';
  existingTasks.forEach(renderProject);
}

// Initial render
renderAllProjects();

// Add new project
document.getElementById('add-project-btn').addEventListener('click', () => {
  const newProject = { id: Date.now(), name: 'Neues Projekt', skills: [] };
  existingTasks.push(newProject);
  renderProject(newProject);
});
