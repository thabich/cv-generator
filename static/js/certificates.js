const skills = JSON.parse(document.getElementById('skills-json').textContent);
const container = document.getElementById('certificates-container');

function renderCertificate(cert) {
  const div = document.createElement('div');
  div.className = 'certificate';
  div.dataset.certId = cert.id;

  div.innerHTML = `
    <h3>${cert.name}</h3>
    <div class="skill-picker"></div>
    <button onclick="editCertificate(${cert.id})">Edit</button>
  `;

  container.appendChild(div);

  // SkillPicker initialisieren
  new SkillPicker(div.querySelector('.skill-picker'), skills, cert.skills || []);
}

function editCertificate(id) {
  const cert = existingCertificates.find(c => c.id === id);
  if (!cert) return alert('Zertifikat nicht gefunden');
  console.log('Edit Certificate', cert);
}

function renderAllCertificates() {
  container.innerHTML = '';
  existingCertificates.forEach(renderCertificate);
}

// Initial render
renderAllCertificates();
