document.addEventListener("DOMContentLoaded", function () {
  const formRegistro = document.getElementById("cadastroForm");
  formRegistro.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita o envio automático do formulário
    const validator = FormValidation.formValidation(formRegistro, {
      fields: {
        nome: {
          validators: {
            notEmpty: {
              message: "O nome é obrigatório",
            },
          },
        },
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
        sobrenome: {
          validators: {
            notEmpty: {
              message: "O sobrenome é obrigatório",
            },
          },
        },
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
            callback: {
              message: "Por favor digite uma senha forte",
              callback: function (input) {
                if (input.value.length > 0) {
                  return validatePassword();
                }
              },
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
        termos: {
          validators: {
            notEmpty: {
              message: "Você deve aceitar os termos de serviço",
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
        const formData = new FormData(formRegistro);
        fetch(formRegistro.action, {
          method: formRegistro.method,
          body: formData,
          headers: {
            "X-CSRFToken": formRegistro.querySelector("[name=csrfmiddlewaretoken]")
              .value,
          },
        })
          .then((response) => response.json())
          .then((res) => {
            if (res.success) {
              Swal.fire("Sucesso!", res.message, "success");
              setInterval(() => {
                location.href = "/home/";
              }, 1000);
            } else {
              Swal.fire("Erro!", res.message, "error");
            }
          })
          .catch((error) => {
            Swal.fire("Erro!", "Ocorreu um erro ao salvar o produto.", "error");
          });
      } else {
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


  const formLogin = document.getElementById("loginForm");
  formLogin.addEventListener("submit", function (event) {
    event.preventDefault();
    const validator2 = FormValidation.formValidation(formLogin, {
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
          senha: {
            validators: {
              notEmpty: {
                message: "A senha é obrigatória",
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
    validator2.validate().then(function (status) {
        if (status === "Valid") {
            const formData = new FormData(formLogin);
            fetch(formLogin.action, {
              method: formLogin.method,
              body: formData,
              headers: {
                "X-CSRFToken": formLogin.querySelector("[name=csrfmiddlewaretoken]")
                  .value,
              },
            })
              .then((response) => response.json())
              .then((res) => {
                if (res.success) {
                  Swal.fire("Sucesso!", res.message, "success");
                  setInterval(() => {
                    location.href = "/home/";
                  }, 1000);
                } else {
                  Swal.fire("Erro!", res.message, "error");
                }
              })
              .catch((error) => {
                Swal.fire("Erro!", "Ocorreu um erro ao salvar o produto.", "error");
              });
        } else {
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

  })
});
