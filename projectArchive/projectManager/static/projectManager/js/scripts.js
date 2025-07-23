function setupDynamicFormset(containerId, formPrefix) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const totalFormsInput = document.querySelector(`input[name="${formPrefix}-TOTAL_FORMS"]`);
  if (!totalFormsInput) return;

  // Class for each form block, e.g. team-members-form
  const formClass = formPrefix.replace(/_/g, '-') + '-form';

  // Update form headings, attributes, and management form count
  function updateAllForms() {
    const forms = container.querySelectorAll(`.${formClass}`);
    forms.forEach((form, index) => {
      // Update heading text: capitalize prefix, remove trailing 's' (plural)
      const heading = form.querySelector('.form-heading');
      if (heading) {
        let displayName = formPrefix.replace(/_/g, ' ');
        if (displayName.endsWith('s')) {
          displayName = displayName.slice(0, -1); // remove trailing 's'
        }
        displayName = displayName.replace(/\b\w/g, c => c.toUpperCase()); // capitalize words
        heading.textContent = `${displayName} ${index + 1}`;
      }

      // Update all input and label attributes with correct index
      form.querySelectorAll('input, label').forEach(el => {
        if (el.name) {
          el.name = el.name.replace(new RegExp(`${formPrefix}-\\d+`), `${formPrefix}-${index}`);
        }
        if (el.id) {
          const newId = el.id.replace(new RegExp(`${formPrefix}-\\d+`), `${formPrefix}-${index}`);
          el.id = newId;
          if (el.tagName.toLowerCase() === 'label' && el.htmlFor) {
            el.htmlFor = newId;
          }
        }
      });
    });
    totalFormsInput.value = forms.length;

    // Show/hide remove buttons (hide if only 1 form)
    const removeButtons = container.querySelectorAll(`.remove-${formPrefix}`);
    if (forms.length <= 1) {
      removeButtons.forEach(btn => btn.classList.add('d-none'));
    } else {
      removeButtons.forEach(btn => btn.classList.remove('d-none'));
    }
  }

  // Add/remove button handlers on container
  container.addEventListener('click', (event) => {
    const target = event.target.closest('button');
    if (!target) return;

    // Add button?
    if (target.classList.contains(`add-${formPrefix}`)) {
      event.preventDefault();
      const currentForm = target.closest(`.${formClass}`);
      if (!currentForm) return;

      const forms = container.querySelectorAll(`.${formClass}`);
      const firstForm = forms[0];
      const newForm = firstForm.cloneNode(true);

      // Clear inputs
      newForm.querySelectorAll('input').forEach(input => {
        if (input.type === 'checkbox' || input.type === 'radio') {
          input.checked = false;
        } else {
          input.value = '';
        }
      });

      // Insert new form after current form
      currentForm.after(newForm);

      updateAllForms();
    }

    // Remove button?
    if (target.classList.contains(`remove-${formPrefix}`)) {
      event.preventDefault();
      const currentForm = target.closest(`.${formClass}`);
      if (!currentForm) return;

      const forms = container.querySelectorAll(`.${formClass}`);
      if (forms.length <= 1) return; // Don't remove last

      currentForm.remove();
      updateAllForms();
    }
  });

  // Initialize on page load
  updateAllForms();
}

document.addEventListener('DOMContentLoaded', () => {
  setupDynamicFormset('team-member-forms', 'team_members');
  setupDynamicFormset('approver-forms', 'approvers');
  setupDynamicFormset('webpage-forms', 'webpages');
});
