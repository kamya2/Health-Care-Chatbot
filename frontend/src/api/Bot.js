import { getApiCall } from '../utils/Api';

// eslint-disable-next-line import/prefer-default-export
export const searchQuery = async (text) => {
  const result = await getApiCall(`/search-answer?q=${text || ''}`);
  return result.data;
};
