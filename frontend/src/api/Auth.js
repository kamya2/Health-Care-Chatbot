import { postApiCall, getApiCall } from '../utils/Api';

export const registerUser = async (userData) => {
  try {
    const response = await postApiCall('/register', userData);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const loginUser = async (userData) => {
  try {
    const response = await postApiCall('/login', userData);
    return { success: true, data: response?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const validateSession = async () => {
  try {
    await getApiCall('/validate_session');
    return { success: true };
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.message || 'User session expired or not logged in.',
    };
  }
};

export const logoutUser = async () => {
  try {
    const response = await postApiCall('/logout', {});
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};
