export function SearchHeader () {
    function addSearchResult(resultText) {
        const resultsElement = document.querySelector('[data-kt-search-element="results"]');
    
        // Limpa os resultados anteriores
        resultsElement.innerHTML = "";
    
        // Cria um novo item de resultado
        let resultItem = document.createElement("div");
        resultItem.classList.add("result-item");
        resultItem.innerHTML = `<span class="result-text">${resultText}</span>`;
    
        // Adiciona o novo item ao container de resultados
        resultsElement.appendChild(resultItem);
    
        // Mostra os resultados e oculta a mensagem de "nenhum resultado"
        resultsElement.classList.remove("d-none");
        emptyElement.classList.add("d-none");
    }
    var processs = function(search) {
        var timeout = setTimeout(function() {
            var query = document.querySelector('[data-kt-search-element="input"]').value;
    
            if (query.length < 2) {
                // Se o usuário não digitou o suficiente, mostra "nenhum resultado"
                resultsElement.classList.add("d-none");
                emptyElement.classList.remove("d-none");
            } else {
                // Adiciona resultados dinamicamente
                addSearchResult(`🔍 Resultado encontrado para: "${query}"`);
                console.log(query)
                // Mostra os resultados
                resultsElement.classList.remove("d-none");
                emptyElement.classList.add("d-none");
            }
    
            // Completa a busca
            search.complete();
        }, 1500);
    }
    
    var clear = function(search) {
        // Hide results
        resultsElement.classList.add("d-none");
        // Hide empty message
        emptyElement.classList.add("d-none");
    }
    
    // Input handler
    const handleInput = () => {
        // Select input field
        const inputField = element.querySelector("[data-kt-search-element='input']");
    
        // Handle keyboard press event
        inputField.addEventListener("keydown", e => {
            // Only apply action to Enter key press
            if(e.key === "Enter"){
                e.preventDefault(); // Stop form from submitting
            }
        });
    }
    
    // Elements
    const element = document.querySelector('#kt_docs_search_handler_basic');
    
    if (!element) {
        return;
    }
    
    const wrapperElement = element.querySelector("[data-kt-search-element='wrapper']");
    const resultsElement = element.querySelector("[data-kt-search-element='results']");
    const emptyElement = element.querySelector("[data-kt-search-element='empty']");
    
    // Initialize search handler
    const searchObject = new KTSearch(element);
    
    // Search handler
    searchObject.on("kt.search.process", processs);
    
    // Clear handler
    searchObject.on("kt.search.clear", clear);
    
    // Handle select
    KTUtil.on(element, "[data-kt-search-element='customer']", "click", function() {
        //modal.hide();
    });
    
    // Handle input enter keypress
    handleInput();
}