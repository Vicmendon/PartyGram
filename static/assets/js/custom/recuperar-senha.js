document.addEventListener("DOMContentLoaded", function () {
  function addSpinner(btn) {
    if (btn.classList.contains("spinner-active")) {
      const html = btn.getAttribute("data-html");
      btn.innerHTML = html;
      btn.disabled = false;
      btn.classList.remove("spinner-active");
    } else {
      const spinner = `<div class="spinner-border p-0" role="status"><span class="visually-hidden">Loading...</span></div>`;
      btn.setAttribute("data-html", btn.innerHTML);
      btn.innerHTML = spinner;
      btn.disabled = true;
      btn.classList.add("spinner-active");
    }
  }
  const RecuperarForm = document.getElementById("RecuperarForm");
  RecuperarForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita o envio automático do formulário
    const submit_button = RecuperarForm.querySelector("button[type=submit]");
    addSpinner(submit_button);
    const validator = FormValidation.formValidation(RecuperarForm, {
      fields: {
        senha: {
          validators: {
            notEmpty: {
              message: "A senha é obrigatória",
            },
            stringLength: {
              min: 8,
              message: "A senha deve ter pelo menos 8 caracteres",
            },
            regexp: {
              regexp: /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*!?]).{8,}$/,
              message:
                "A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial (@, #, $, etc.)",
            },
          },
        },
        confirm_senha: {
          validators: {
            notEmpty: {
              message: "A confirmação de senha é obrigatória",
            },
            identical: {
              compare: function () {
                return form.querySelector('[name="senha"]').value;
              },
              message: "As senhas devem ser iguais",
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
        const formData = new FormData(RecuperarForm);
        fetch(RecuperarForm.action, {
          method: RecuperarForm.method,
          body: formData,
          headers: {
            "X-CSRFToken": RecuperarForm.querySelector(
              "[name=csrfmiddlewaretoken]"
            ).value,
          },
        })
          .then((response) => response.json())
          .then((res) => {
            if (res.success) {
              Swal.fire("Sucesso!", res.message, "success");
              setInterval(() => {
                location.href = `/users/auth/login`;
              }, 1000);
            } else {
              Swal.fire("Erro!", res.message, "error");
              addSpinner(submit_button);
            }
          })
          .catch((error) => {
            Swal.fire(
              "Erro!",
              "Ocorreu um erro ao trocar a senha." + error,
              "error"
            );
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
