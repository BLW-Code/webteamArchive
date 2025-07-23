function setupDynamicFormset(containerId, formPrefix) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const totalFormsInput = document.querySelector(`input[name="${formPrefix}-TOTAL_FORMS"]`);
  if (!totalFormsInput) return;

  const formClass = formPrefix.replace(/_/g, '-') + '-form';  // e.g. team-members-form

  function updateAllForms() {
    const forms = container.querySelectorAll(`.${formClass}`);
    forms.forEach((form, index) => {
      const heading = form.querySelector('.form-heading');
      if (heading) {
        const words = formPrefix.split('_');
        const singularWords = [...words];
        const lastWord = singularWords.pop();
        if (lastWord.endsWith('s')) {
          singularWords.push(lastWord.slice(0, -1));
        } else {
          singularWords.push(lastWord);
        }
        const displayName = singularWords.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
        heading.textContent = `${displayName} ${index + 1}`;
      }
      updateFormAttributes(form, formPrefix, index);
    });
    totalFormsInput.value = forms.length;

    const removeButtons = container.querySelectorAll(`.remove-${formPrefix}`);
    if (forms.length <= 1) {
      removeButtons.forEach(btn => btn.classList.add('d-none'));
    } else {
      removeButtons.forEach(btn => btn.classList.remove('d-none'));
    }
  }

  function updateFormAttributes(form, prefix, index) {
    form.querySelectorAll('input, label').forEach(el => {
      if (el.name) {
        el.name = el.name.replace(new RegExp(`${prefix}-\\d+`), `${prefix}-${index}`);
      }
      if (el.id) {
        const newId = el.id.replace(new RegExp(`${prefix}-\\d+`), `${prefix}-${index}`);
        el.id = newId;

        if (el.tagName.toLowerCase() === 'label' && el.htmlFor) {
          el.htmlFor = newId;
        }
      }
    });
  }

  container.addEventListener('click', (event) => {
    const target = event.target.closest('button'); // button or icon inside
    if (!target) return;

    if (target.classList.contains(`add-${formPrefix}`)) {
      event.preventDefault();

      const currentForm = target.closest(`.${formClass}`);
      if (!currentForm) return;

      const forms = container.querySelectorAll(`.${formClass}`);
      const formCount = forms.length;

      const firstForm = forms[0];
      const newForm = firstForm.cloneNode(true);

      newForm.querySelectorAll('input').forEach(input => {
        if (input.type === 'checkbox' || input.type === 'radio') {
          input.checked = false;
        } else {
          input.value = '';
        }
      });

      currentForm.after(newForm);
      updateAllForms();
    }

    if (target.classList.contains(`remove-${formPrefix}`)) {
      event.preventDefault();

      const currentForm = target.closest(`.${formClass}`);
      if (!currentForm) return;

      const forms = container.querySelectorAll(`.${formClass}`);
      if (forms.length <= 1) return;

      currentForm.remove();
      updateAllForms();
    }
  });

  updateAllForms();
}

document.addEventListener("DOMContentLoaded", () => {
  setupDynamicFormset("team-member-forms", "team_members");
  setupDynamicFormset("approver-forms", "approvers");
  setupDynamicFormset("webpage-forms", "webpages");
});
