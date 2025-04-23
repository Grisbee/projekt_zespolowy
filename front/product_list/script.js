let currentPage = 1;
const itemsPerPage = 24;
let selectedCategories = [];

document.getElementById('search-button').addEventListener('click', ()=>{
  query = document.getElementById('search-input').value.trim();
  console.log(query);

  if(query.length > 0 ){
    searchAndListSelectedProducts(query);
  }
})


async function loadCategories() {
  try {
    const response = await fetch('http://localhost:8081/api/product-list/get-intro-products', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const categories = await response.json();
    createCategoryFilters(categories);
    
  } catch (error) {
    console.error('Nie załadowano listy kategorii z bazy danych:', error);
  }
}


async function loadProducts(page = 1, categories = []) {
  try {
    const response = await fetch('http://localhost:8081/api/product-list/get-products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        page: page,
        limit: itemsPerPage,
        categories: categories
      })
    });

    console.log("Отправляем: page =", page, ", limit =", itemsPerPage);
    
    const data = await response.json();

    console.log("Полный ответ от сервера:", data);
    console.log("Получено продуктов:", data.products.length, "из", data.totalCount);


    displayProducts(data.products);
    setupPagination(data.totalCount, page, categories);
    
  } catch (error) {
    console.error('Error loading products:', error);
  }
}


function createCategoryFilters(categories) {
  const filtersContainer = document.createElement('div');
  filtersContainer.className = 'filters-container';
  
  const filtersTitle = document.createElement('h3');
  filtersTitle.textContent = 'Categories';
  filtersTitle.className = 'filters-title';
  filtersContainer.appendChild(filtersTitle);
  
  const categoriesFlexContainer = document.createElement('div');
  categoriesFlexContainer.className = 'categories-flex-container';
  
  categories.forEach(category => {
    const filterItem = document.createElement('div');
    filterItem.className = 'filter-item';
    
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = `category-${category.toLowerCase().replace(/\s+/g, '-')}`;
    checkbox.value = category;
    checkbox.className = 'category-checkbox';

    checkbox.addEventListener('change', () => {
      const category = checkbox.value;
    
      if (checkbox.checked) {
        if (!selectedCategories.includes(category)) {
          selectedCategories.push(category);
        }
      } else {
        selectedCategories = selectedCategories.filter(c => c !== category);
      }
    
      currentPage = 1; // Сбросим на первую страницу при смене фильтра
      loadProducts(currentPage, selectedCategories);
    });
    
    const label = document.createElement('label');
    label.htmlFor = checkbox.id;
    label.textContent = category;
    
    filterItem.appendChild(checkbox);
    filterItem.appendChild(label);
    categoriesFlexContainer.appendChild(filterItem);
  });
  
  filtersContainer.appendChild(categoriesFlexContainer);
  
  const mainContent = document.querySelector('.main-content');
  mainContent.insertBefore(filtersContainer, mainContent.firstChild);
}



function displayProducts(products) {
  const productsContainer = document.querySelector('.products-container');
  productsContainer.innerHTML = '';

  if (products.length === 0) {
    productsContainer.innerHTML = '<p class="no-products">No products found</p>';
    return;
  }

  console.log("Отрисовываем карточек:", products.length);

  products.forEach(product => {
    const productCard = document.createElement('div');
    productCard.className = 'product-card';
    
    productCard.innerHTML = `
      <div class="product-image">
        ${product.img_url ? `<img src="${product.img_url}" alt="${product.title}">` : 
          '<span class="material-symbols-outlined">image</span>'}
      </div>
      <div class="product-info">
        <h3 class="product-title">${product.title}</h3>
        <div class="product-meta">
          <div class="product-rating">
            <span class="rating-value">Rating: ${product.rating || 'N/A'}</span>
          </div>
          <div class="review-count">${product.review_count || 0} reviews</div>
        </div>
        <p class="product-price">${product.price} ${product.currency}</p>
        <a href="dashboards.html" class="product-generate">
          Generate Dashboard
        </a>
      </div>
    `;
    
    productsContainer.appendChild(productCard);
  });
}


function setupPagination(totalCount, currentPage, categories) {
  const paginationContainer = document.querySelector('.pagination-container') || 
                             document.createElement('div');
  paginationContainer.className = 'pagination-container';
  paginationContainer.innerHTML = '';

  const totalPages = Math.ceil(totalCount / itemsPerPage);

  if (totalPages > 1) {
    // Previous button
    if (currentPage > 1) {
      const prevBtn = document.createElement('button');
      prevBtn.className = 'pagination-btn';
      prevBtn.textContent = 'Previous';
      prevBtn.addEventListener('click', () => {
        loadProducts(currentPage - 1, categories);
      });
      paginationContainer.appendChild(prevBtn);
    }

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
      const pageBtn = document.createElement('button');
      pageBtn.className = `pagination-btn ${i === currentPage ? 'active' : ''}`;
      pageBtn.textContent = i;
      pageBtn.addEventListener('click', () => {
        loadProducts(i, categories);
      });
      paginationContainer.appendChild(pageBtn);
    }

    // Next button
    if (currentPage < totalPages) {
      const nextBtn = document.createElement('button');
      nextBtn.className = 'pagination-btn';
      nextBtn.textContent = 'Next';
      nextBtn.addEventListener('click', () => {
        loadProducts(currentPage + 1, categories);
      });
      paginationContainer.appendChild(nextBtn);
    }
  }

  document.querySelector('.main-content').appendChild(paginationContainer);
}


async function searchAndListSelectedProducts(query) {
  try{
    const response = await fetch('http://localhost:8081/api/product-list/get-selected-category-products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query,
        page: currentPage,
        limit: itemsPerPage
       })
    });

    const data = await response.json();
    console.log(data);

    displayProducts(data.products);
    setupPagination(data.totalCount, 1, selectedCategories);
  } catch (e) {
      console.log(e);
  }
}


document.addEventListener('DOMContentLoaded', () => {
  loadCategories();
  loadProducts();
});