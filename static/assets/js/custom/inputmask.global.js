export function applyEmailValidation() {
  document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todos os mask inputs da página
    document.querySelectorAll('.mask-email').forEach(function (input) {
      // Aplica a máscara de e-mail usando Inputmask
      Inputmask({
        mask: "*{1,20}[.*{1,20}][.*{1,20}][.*{1,20}]@*{1,20}[.*{2,6}][.*{1,2}]",
        greedy: false,
        onBeforePaste: function (pastedValue, opts) {
          pastedValue = pastedValue.toLowerCase();
          return pastedValue.replace("mailto:", "");
        },
        definitions: {
          "*": {
            validator: '[0-9A-Za-z!#$%&"*+/=?^_`{|}~-]',
            cardinality: 1,
            casing: "lower",
          },
        },
      }).mask(input);
    });
  });
}
