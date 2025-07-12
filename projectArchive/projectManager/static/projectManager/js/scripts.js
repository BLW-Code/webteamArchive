function setupDynamicFormset(containerId, addBtnId, formPrefix) {
    const container = document.getElementById(containerId);
    const addBtn = document.getElementById(addBtnId);
    const totalFormsInput = document.querySelector(`input[name="${formPrefix}-TOTAL_FORMS"]`);

    // Add new form
    addBtn.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value);
        const firstForm = container.querySelector(`.${formPrefix}-form`);
        if (!firstForm) return;

        const newForm = firstForm.cloneNode(true);

        // Clear input values
        newForm.querySelectorAll("input").forEach(input => {
            if (input.type === "checkbox" || input.type === "radio") {
                input.checked = false;
            } else {
                input.value = "";
            }
        });

        // Update names, ids, and labels
        updateFormAttributes(newForm, formPrefix, formCount);

        container.appendChild(newForm);
        totalFormsInput.value = formCount + 1;

        attachRemoveButtons();
    });

    function attachRemoveButtons() {
        const forms = container.querySelectorAll(`.${formPrefix}-form`);
        const removeButtons = container.querySelectorAll(`.remove-${formPrefix}`);

        if (forms.length <= 1) {
            removeButtons.forEach(btn => btn.classList.add('d-none'));
        } else {
            removeButtons.forEach(btn => btn.classList.remove('d-none'));
        }

        removeButtons.forEach(btn => {
            btn.onclick = () => {
                if (forms.length > 1) {
                    btn.closest(`.${formPrefix}-form`).remove();
                    updateAllFormIndexes();
                    attachRemoveButtons();  // update visibility after removal
                }
            };
        });
    }

    function updateFormAttributes(form, formPrefix, index) {
        // Update all inputs and labels inside the form
        form.querySelectorAll("input, label").forEach(el => {
            // Update 'name' attribute
            if (el.name) {
                el.name = el.name.replace(new RegExp(`${formPrefix}-\\d+`), `${formPrefix}-${index}`);
            }
            // Update 'id' attribute
            if (el.id) {
                const oldId = el.id;
                const newId = oldId.replace(new RegExp(`${formPrefix}-\\d+`), `${formPrefix}-${index}`);
                el.id = newId;

                // If this is a label, update its 'for' attribute too
                if (el.tagName.toLowerCase() === 'label' && el.htmlFor) {
                    el.htmlFor = newId;
                }
            }
        });
    }

    function updateAllFormIndexes() {
        const forms = container.querySelectorAll(`.${formPrefix}-form`);
        forms.forEach((form, index) => {
            updateFormAttributes(form, formPrefix, index);
        });
        totalFormsInput.value = forms.length;
    }

    // Initialize remove buttons on page load
    attachRemoveButtons();
}

document.addEventListener("DOMContentLoaded", () => {
    setupDynamicFormset("team-member-forms", "add-team-member", "team_members");
    setupDynamicFormset("approver-forms", "add-approver", "approvers");
    setupDynamicFormset("webpage-forms", "add-webpage", "webpages");
});
