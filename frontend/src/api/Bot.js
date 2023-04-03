import { deleteApiCall, getApiCall, postApiCall } from '../utils/Api';

export const createConversation = async () => {
  try {
    const response = await postApiCall('/conversation', {});
    return { success: true, data: response?.data?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const deleteConversation = async (conversationId) => {
  try {
    const response = await deleteApiCall(`/conversation/${conversationId}`);
    return { success: true, data: response?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const getConversations = async () => {
  try {
    const response = await getApiCall('/conversation');

    return { success: true, data: response?.data?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const getConversationMessages = async (conversationId) => {
  try {
    const response = await getApiCall(`/message/${conversationId}`);

    return { success: true, data: response?.data?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const postMessage = async (conversationId, message) => {
  try {
    const response = await postApiCall(`/message/${conversationId}`, { message });
    return { success: true, data: response?.data?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};

export const searchQuery = async (payload) => {
  try {
    const response = await postApiCall(`/search-answer`, payload);
    return { success: true, data: response?.data };
  } catch (error) {
    return { success: false, message: error?.response?.data?.message || 'Something went wrong' };
  }
};
