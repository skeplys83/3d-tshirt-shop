import {get} from "svelte/store";
import {apiUrl, csrfToken} from "../../stores/global_stores.js";
import axios from "axios";
import {getCsrfToken} from "$lib/index.js";

export async function getProducts() {
    try {
        const response = await axios.get(`${apiUrl}/api/v1/products/`, {
            withCredentials: true,
        });

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('There are no products available');
    }
}

export async function putProduct(productId, name, description, price, stripePriceId, stock, colors, category, discount, discountInPercent) {
    try {
        let token = get(csrfToken);
        if (!token) {
            token = getCsrfToken();
            if (token) {
                csrfToken.set(token);
            }
        }

        if (!token) {
            return;
        }

        const response = await axios.put(`${apiUrl}/api/v1/products/${productId}/`, {
            name: name,
            description: description,
            price: price,
            stripePriceId: stripePriceId,
            stock: stock,
            colors: colors,
            category: category,
            discount: discount,
            discountInPercent: discountInPercent
        }, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': token,
                'Content-Type': 'application/json',
            },
        });

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Update product failed');
    }
}


export async function uploadProductFiles(productId, productPicture, productBlenderModel) {
    try {
        let token = get(csrfToken);
        if (!token) {
            token = getCsrfToken();
            if (token) {
                csrfToken.set(token);
            }
        }

        if (!token) {
            return;
        }

        // JSON für die PATCH-Anfrage erstellen
        const payload = {
            ...(productPicture && {productPicture}),
            ...(productBlenderModel && {productBlenderModel})
        };

        const response = await axios.patch(`${apiUrl}/api/v1/products/${productId}/`, payload, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': token,
                'Content-Type': 'application/json',
            },
        });

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('File upload failed');
    }
}

export async function postProduct(name, description, price, stripePriceId, stock, colors, category, discount, discountInPercent, productPicture, productBlenderModel) {
    try {
        let token = get(csrfToken);
        if (!token) {
            token = getCsrfToken();
            if (token) {
                csrfToken.set(token);
            }
        }

        if (!token) {
            return;
        }

        const response = await axios.post(`${apiUrl}/api/v1/products/`, {
            name: name,
            description: description,
            price: price,
            stripePriceId: stripePriceId,
            stock: stock,
            colors: colors,
            category: category,
            discount: discount,
            discountInPercent: discountInPercent,
            productPicture: productPicture,
            productBlenderModel: productBlenderModel
        }, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': token,
                'Content-Type': 'application/json',
            },
        });

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Create product failed');
    }
}

export async function deleteProduct(productId){
    try {
      const token = get(csrfToken);
  
        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }
  
      const response = await axios.delete(`${apiUrl}/api/v1/products/${productId}/`, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': token,
        },
      })
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('The product could not be deleted');
    }
  }