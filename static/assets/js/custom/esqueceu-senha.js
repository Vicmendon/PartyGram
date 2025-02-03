document.addEventListener("DOMContentLoaded", function () {
  function addSpinner(btn) {
    if (btn.classList.contains("spinner-active")) {
      const html = btn.getAttribute("data-html");
      btn.innerHTML = html;
      btn.disabled = false;
      btn.classList.remove("spinner-active");
    } else {
      const spinner = `<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>`;
      btn.setAttribute("data-html", btn.innerHTML);
      btn.innerHTML = spinner;
      btn.disabled = true;
      btn.classList.add("spinner-active");
    }
  }
  const formEnviarCode = document.getElementById("EnviarCodeForm");
  formEnviarCode.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita o envio automático do formulário
    const submit_button = formEnviarCode.querySelector("button[type=submit]");
    addSpinner(submit_button);
    const validator = FormValidation.formValidation(formEnviarCode, {
      fields: {
        email: {
          validators: {
            notEmpty: {
              message: "O campo de e-mail é obrigatório",
            },
            emailAddress: {
              message: "O formato do e-mail está incorreto",
            },
          },
        },
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger({
          event: "input",
        }),
        bootstrap: new FormValidation.plugins.Bootstrap5({
          rowSelector: ".fv-row",
          eleInvalidClass: "is-invalid",
          eleValidClass: "is-valid",
        }),
      },
    });
    validator.validate().then(function (status) {
      if (status === "Valid") {
        // Se tudo estiver correto, faz a requisição
        const formData = new FormData(formEnviarCode);
        fetch(formEnviarCode.action, {
          method: formEnviarCode.method,
          body: formData,
          headers: {
            "X-CSRFToken": formEnviarCode.querySelector(
              "[name=csrfmiddlewaretoken]"
            ).value,
          },
        })
          .then((response) => response.json())
          .then((res) => {
            if (res.success) {
              Swal.fire("Sucesso!", res.message, "success");
              const conteiner_code = document.getElementById("conteiner_code");
              conteiner_code.classList.remove("d-none");
              const input_email = formEnviarCode.querySelector("[name=email]");
              input_email.disabled = true;
              submit_button.classList.add("d-none");
              const title = formEnviarCode.querySelector("h4");
              title.classList.add("d-none");
            } else {
              Swal.fire("Erro!", res.message, "error");
              addSpinner(submit_button);
            }
          })
          .catch((error) => {
            Swal.fire("Erro!", "Ocorreu um erro ao enviar codigo." + error, "error");
            addSpinner(submit_button);
          });
      } else {
        addSpinner(submit_button);
        Swal.fire({
          text: "Por favor, corrija os erros antes de continuar.",
          icon: "error",
          buttonsStyling: false,
          confirmButtonText: "Ok, entendi!",
          customClass: {
            confirmButton: "btn btn-primary",
          },
        });
      }
    });
  });
  const CodeForm = document.getElementById("CodeForm");
  CodeForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita o envio automático do formulário
    const submit_button = CodeForm.querySelector("button[type=submit]");
    addSpinner(submit_button);
    const validator = FormValidation.formValidation(CodeForm, {
      fields: {
        code: {
          validators: {
            notEmpty: {
              message: "O codigo precisa ser informado",
            },
            stringLength: {
                min: 6,
                max: 6,
                message: "O código deve ter exatamente 6 caracteres",
            },
          },
        },
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger({
          event: "input",
        }),
        bootstrap: new FormValidation.plugins.Bootstrap5({
          rowSelector: ".fv-row",
          eleInvalidClass: "is-invalid",
          eleValidClass: "is-valid",
        }),
      },
    });
    validator.validate().then(function (status) {
      if (status === "Valid") {
        // Se tudo estiver correto, faz a requisição
        fetch(CodeForm.action, {
          method: 'PUT',
          body: JSON.stringify({
            email: formEnviarCode.querySelector("[name=email]").value,
            code: CodeForm.querySelector("[name=code]").value,
          }),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CodeForm.querySelector(
              "[name=csrfmiddlewaretoken]"
            ).value,
          },
        })
          .then((response) => response.json())
          .then((res) => {
            if (res.success) {
              Swal.fire("Sucesso!", res.message, "success");
              setInterval(() => {
                location.href = `/users/auth/recovery/${res.hash}`;
              }, 1000);
            } else {
              Swal.fire("Erro!", res.message, "error");
              addSpinner(submit_button);
            }
          })
          .catch((error) => {
            Swal.fire("Erro!", "Ocorreu um erro ao enviar codigo." + error, "error");
            addSpinner(submit_button);
          });
      } else {
        addSpinner(submit_button);
        Swal.fire({
          text: "Por favor, corrija os erros antes de continuar.",
          icon: "error",
          buttonsStyling: false,
          confirmButtonText: "Ok, entendi!",
          customClass: {
            confirmButton: "btn btn-primary",
          },
        });
      }
    });
  });
});
