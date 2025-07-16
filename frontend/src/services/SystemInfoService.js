class SystemInfoService {
  static collectSystemInfo() {
    try {
      const os = window.require('os');
      const crypto = window.require('crypto');
      const osType = os.type();
      let osName = osType;

      if (osType === 'Darwin') osName = 'darwin';
      else if (osType === 'Windows_NT') osName = 'windows';
      else if (osType === 'Linux') osName = 'linux';
      const userInfo = os.userInfo();
      const hostname = os.hostname();
      const systemData =
        os.type() + os.arch() + os.hostname() + userInfo.username;
      const hwid = crypto.createHash('md5').update(systemData).digest('hex');
      const info = {
        user: userInfo.username || '',
        computer: hostname ? hostname.toLowerCase() : '',
        domain: process.env.USERDOMAIN || process.env.DOMAIN || '',
        name: userInfo.username || '',
        hwid: hwid || '',
        os: osName || '',
        osVersion: os.release() || '',
      };

      return info;
    } catch (error) {
      console.error('Error gathering system information:', error);

      return {
        user: '',
        computer: '',
        domain: '',
        name: '',
        hwid: '',
        os: '',
        osVersion: '',
        error: 'Error accessing system information',
      };
    }
  }

  static getTimezoneOffset() {
    const timezoneOffsetMinutes = new Date().getTimezoneOffset();

    return -timezoneOffsetMinutes * 60 * 1000;
  }
}

export default SystemInfoService;
