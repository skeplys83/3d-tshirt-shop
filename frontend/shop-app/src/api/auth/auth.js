import axios from 'axios';
import { csrfToken, apiUrl } from "../../stores/global_stores.js";
import { get } from 'svelte/store';
import {setCsrfToken} from "$lib";

export async function login(email, password) {
  try {
    const response = await axios.post(`${apiUrl}/api/v1/auth/login/`, {
      email,
      password,
    },
    {
      withCredentials: true
    });
    setCsrfToken();
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      throw new Error("Invalid email or password.");
    }
    throw error.response ? error.response.data : new Error("Login failed");
  }
}

export async function logout() {
    try {
        const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }

        const response = await axios.post(`${apiUrl}/api/v1/auth/logout/`,{},{
            withCredentials: true,
            headers: {
                'X-CSRFToken': token,
            },
        });

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Logout failed');
    }
}

export async function register(email, salutation, firstName, lastName, password, dateOfBirth, phoneNumber, streetAndNumber, postalCode, city, country) {
    try {
      const response = await axios.post(
          `${apiUrl}/api/v1/auth/register/`,
        {
          email: email,
          salutation: salutation,
          first_name: firstName,
          last_name: lastName,
          date_of_birth: dateOfBirth,
          phone_number: phoneNumber,
          street_and_number: streetAndNumber,
          postal_code: postalCode,
          city: city,
          country: country,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Registration failed');
    }
  }

  export async function getUser(userID){
    try {
      const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }

      const response = await axios.get(`${apiUrl}/api/v1/auth/${userID}/`, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': token,
        },
      });
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Userinfo not available');
    }
  }

  export async function getAllUsers(){
    try {
        const token = get(csrfToken);
        if (!token){
            return;
        }
        const response = await axios.get(`${apiUrl}/api/v1/auth/`, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': token,
            },
        });
        return response.data;
    }catch (error){
        throw error.response ? error.response.data : new Error('No users available');
    }
  }

  export async function getUserInfo(){
    try {
      const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }

      const response = await axios.get(`${apiUrl}/api/v1/auth/info/`, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': token,
        },
      });
      return response.data;
    } catch (error) {
        if (error.response && error.response.status === 403) {
          console.warn('User is not authenticated');
          return null;
      }
        throw error.response ? error.response.data : new Error('Userinfo not available');
    }
  }

  export async function patchUser(userID, valueStaff, valueActive, valueFirstName, valueLastName, valueEmail){
      try {
          const token = get(csrfToken);

          if (!token) {
              console.error('CSRF-Token not found');
              return;
          }
          console.log({
              is_active: valueActive,
              is_staff: valueStaff,
              email: valueEmail,
              first_name: valueFirstName,
              last_name: valueLastName
          })
          const response = await axios.patch(`${apiUrl}/api/v1/auth/${userID}/`, {
              is_active: valueActive,
              is_staff: valueStaff,
              email: valueEmail,
              first_name: valueFirstName,
              last_name: valueLastName
          },
              {
                  withCredentials: true,
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': token,
                  },
              });
          console.log(response.data)
          return response.data;
      } catch (error) {
          throw error.response ? error.response.data : new Error('User Profile Update failed');
      }
  }

  export async function updateUser(userID, email, salutation, firstName, lastName, dateOfBirth, phoneNumber, streetAndNumber, postalCode, city, country) {
    try {
      const token = get(csrfToken);

        if (!token) {
            console.error('CSRF-Token not found');
            return;
        }

      const response = await axios.put(
          `${apiUrl}/api/v1/auth/${userID}/`,
        {
          email: email,
          salutation: salutation,
          first_name: firstName,
          last_name: lastName,
          date_of_birth: dateOfBirth,
          phone_number: phoneNumber,
          street_and_number: streetAndNumber,
          postal_code: postalCode,
          city: city,
          country: country
        },
        {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token,
          },
        }
      );
      return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('User Profile Update failed');
    }
  }
  