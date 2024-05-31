import api from './api';

const AccountsAPI = {
  async getUsers() {
    try {
      const response = await api.get('accounts/users/');
      return response.data;
    } catch (error) {
      console.error("유저 정보를 가져오는 중 오류가 발생했습니다 : ", error);
      throw error;
    }
  },
};

export default AccountsAPI;