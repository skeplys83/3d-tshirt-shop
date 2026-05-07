import axios from 'axios';
import {csrfToken, apiUrl, userId} from "../../stores/global_stores.js";
import { get } from 'svelte/store';

export async function getOrdersFromUser(userID){
    try {
      const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }

      const response = await axios.get(`${apiUrl}/api/v1/orders/user/${userID}/`, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': token,
        },
      })
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('There are no orders for this user yet');
    }
  }

  export async function getAllOrders(){
    try {
      const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }

      const response = await axios.get(`${apiUrl}/api/v1/orders/`, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': token,
        },
      });
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('There might be no orders or any error occurred');
    }
  }

export async function postNewOrder(json) {
    try {
        const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }
        const response = await axios.post(`${apiUrl}/api/v1/orders/`, {
                salutation: json.salutation,
                first_name: json.firstName,
                last_name: json.lastName,
                email: json.email,
                phone_number: json.phoneNumber,
                street_and_number: json.streetAndNumber,
                city: json.city,
                postal_code: json.postalCode,
                country: json.country,
                differentShippingAddress: json.differentShippingAddress,
                alternative_address: {
                    street_and_number: json.alternativeAddress.streetAndNumber,
                    city: json.alternativeAddress.city,
                    postal_code: json.alternativeAddress.postalCode,
                    country: json.alternativeAddress.country,
                },
                termsAccepted: json.termsAccepted,
                totalPrice: json.totalPrice,
                selectedProducts: json.selectedProducts,
            },
            {
                withCredentials: true,
                headers: {
                    'X-CSRFToken': token,
                },
            });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Error while poblishing new order');
    }
}

export async function updateOrder(userID, alternative_address, city, country, differentShippingAddress, email, first_name, last_name, phoneNumber, postal_code, payedStatus, paymentMethod, salutation, selectedProducts, street_and_number, termsAccepted, totalPrice, orderPlacedByUserWithId, stripeSessionID, status){
  try {
    const token = get(csrfToken);

    if (!token) {
        console.error('CSRF-Token not found');
        return;
    }

    const response = await axios.put(`${apiUrl}/api/v1/orders/${userID}/`, {
                salutation: salutation,
                first_name: first_name,
                last_name: last_name,
                email: email,
                phone_number: phoneNumber,
                street_and_number: street_and_number,
                city: city,
                postal_code: postal_code,
                country: country,
                differentShippingAddress: differentShippingAddress,
                alternative_address: {
                    street_and_number: alternative_address.street_and_number,
                    city: alternative_address.city,
                    postal_code: alternative_address.postal_code,
                    country: alternative_address.country,
                },
                termsAccepted: termsAccepted,
                totalPrice: totalPrice,
                selectedProducts: selectedProducts,
                payedStatus: payedStatus,
                paymentMethod: paymentMethod,
                orderPlacedByUserWithId: orderPlacedByUserWithId,
                stripe_session_id: stripeSessionID,
                status: status,
      },
      {
          withCredentials: true,
          headers: {
              'X-CSRFToken': token,
          },
      });
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Error while updating order');
    }
}

export async function deleteOrder(orderID){
  try {
    const token = get(csrfToken);

      if (!token) {
          console.error('CSRF-Token not found');
          return;
      }

    const response = await axios.delete(`${apiUrl}/api/v1/orders/${orderID}/`, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': token,
      },
    })
    return response.data;
  } catch (error) {
      throw error.response ? error.response.data : new Error('The order could not be deleted');
  }
}