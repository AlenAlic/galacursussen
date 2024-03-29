// email
const validateEmail = email => {
  // eslint-disable-next-line no-useless-escape
  let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

// password strength
const strongRegex = new RegExp(
  "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{16,})" // eslint-disable-line no-useless-escape
);
const mediumRegex = new RegExp(
  "^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{12,})"
);
const weakRegex = new RegExp("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})");

// price formatting
const currencyFormat = num => {
  let sign = num >= 0 ? "€" : "-€";
  num = Math.abs(num);
  if (num !== 0) {
    return (
      sign +
      num
        .toFixed(2)
        .replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
        .replace(".00", "")
    );
  } else {
    return "-";
  }
};

// available years
const availableYears = () => {
  const YEAR = 2018;
  const range = n => [...Array(n).keys()];
  let now = new Date();
  let year = now.getFullYear();
  if (now.getMonth() < 7) year = year - 1;
  return range(year - YEAR + 2).map(r => r + YEAR);
};

// filter for courses by committee (InCie/SalCie)
const filterCoursesByCommittee = (c, u) => {
  if ((u.incie && u.salcie) || u.mucie || u.organizer || u.admin) return c;
  if (u.incie) return c.committee_value === "incie";
  if (u.salcie) return c.committee_value === "salcie";
};

const UtilitiesHandler = {
  install(Vue) {
    Vue.prototype.$util = {
      getScreenSize: function() {
        return window.innerWidth;
      },
      // check for screen width
      isScreenLargeEnough: function() {
        return this.getScreenSize() > 1200;
      },
      splitEmail: function(email) {
        let at = email.lastIndexOf("@");
        if (at < 0) return email;
        return email.substring(0, at) + "\u200B" + email.substring(at);
      }
    };
  }
};

export default UtilitiesHandler;

export {
  validateEmail,
  strongRegex,
  mediumRegex,
  weakRegex,
  currencyFormat,
  availableYears,
  filterCoursesByCommittee,
  UtilitiesHandler
};
