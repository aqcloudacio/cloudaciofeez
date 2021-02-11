/*!
 * v-currency-field v3.1.1 
 * (c) 2020 Philipe Augusto <phiny1@gmail.com>
 * Released under the MIT License.
 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (global = global || self, factory(global.VCurrencyField = {}));
}(this, (function (exports) { 'use strict';

  function _typeof(obj) {
    "@babel/helpers - typeof";

    if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
      _typeof = function (obj) {
        return typeof obj;
      };
    } else {
      _typeof = function (obj) {
        return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
      };
    }

    return _typeof(obj);
  }

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function ownKeys(object, enumerableOnly) {
    var keys = Object.keys(object);

    if (Object.getOwnPropertySymbols) {
      var symbols = Object.getOwnPropertySymbols(object);
      if (enumerableOnly) symbols = symbols.filter(function (sym) {
        return Object.getOwnPropertyDescriptor(object, sym).enumerable;
      });
      keys.push.apply(keys, symbols);
    }

    return keys;
  }

  function _objectSpread2(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {};

      if (i % 2) {
        ownKeys(Object(source), true).forEach(function (key) {
          _defineProperty(target, key, source[key]);
        });
      } else if (Object.getOwnPropertyDescriptors) {
        Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
      } else {
        ownKeys(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
    }

    return target;
  }

  function _objectWithoutPropertiesLoose(source, excluded) {
    if (source == null) return {};
    var target = {};
    var sourceKeys = Object.keys(source);
    var key, i;

    for (i = 0; i < sourceKeys.length; i++) {
      key = sourceKeys[i];
      if (excluded.indexOf(key) >= 0) continue;
      target[key] = source[key];
    }

    return target;
  }

  function _objectWithoutProperties(source, excluded) {
    if (source == null) return {};

    var target = _objectWithoutPropertiesLoose(source, excluded);

    var key, i;

    if (Object.getOwnPropertySymbols) {
      var sourceSymbolKeys = Object.getOwnPropertySymbols(source);

      for (i = 0; i < sourceSymbolKeys.length; i++) {
        key = sourceSymbolKeys[i];
        if (excluded.indexOf(key) >= 0) continue;
        if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
        target[key] = source[key];
      }
    }

    return target;
  }

  var dispatchEvent = (function (el, eventName, data) {
    var event = document.createEvent('CustomEvent');
    event.initCustomEvent(eventName, true, true, data);
    el.dispatchEvent(event);
  });

  /**
   * Sets the value of an input programmatically.
   *
   * @param {HTMLInputElement} el The input element the `v-currency` directive is bound to.
   * @param {Number} value The number to be set.
   */

  var setValue = function setValue(el, value) {
    return dispatchEvent(el, 'format', {
      value: value
    });
  };

  /**
   * Vue Currency Input 1.21.0
   * (c) 2018-2020 Matthias Stiller
   * @license MIT
   */
  function dispatchEvent$1(el, eventName, data) {
    var event = document.createEvent('CustomEvent');
    event.initCustomEvent(eventName, true, true, data);
    el.dispatchEvent(event);
  }

  var toExternalNumberModel = function toExternalNumberModel(number, valueAsInteger, fractionDigits) {
    return valueAsInteger && number != null ? Number(number.toFixed(fractionDigits).split('.').join('')) : number;
  };

  var DEFAULT_OPTIONS = {
    locale: undefined,
    currency: 'EUR',
    valueAsInteger: false,
    distractionFree: true,
    precision: undefined,
    autoDecimalMode: false,
    valueRange: undefined,
    allowNegative: true
  };

  var getValue = function getValue(el) {
    var ref = el.$ci;
    var numberValue = ref.numberValue;
    var currencyFormat = ref.currencyFormat;
    var options = ref.options;
    return toExternalNumberModel(numberValue, options.valueAsInteger, currencyFormat.maximumFractionDigits);
  };

  var setValue$1 = function setValue(el, value) {
    return dispatchEvent$1(el, 'format', {
      value: value
    });
  };

  var escapeRegExp = function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  };

  var removeLeadingZeros = function removeLeadingZeros(str) {
    return str.replace(/^0+(0$|[^0])/, '$1');
  };

  var count = function count(str, search) {
    return (str.match(new RegExp(escapeRegExp(search), 'g')) || []).length;
  };

  var startsWith = function startsWith(str, search) {
    return str.substring(0, search.length) === search;
  };

  var substringBefore = function substringBefore(str, search) {
    return str.substring(0, str.indexOf(search));
  };

  var setCaretPosition = function setCaretPosition(el, position) {
    return el.setSelectionRange(position, position);
  };

  var getCaretPositionAfterFormat = function getCaretPositionAfterFormat(newValue, inputtedValue, caretPosition, numberFormat, options) {
    var prefix = numberFormat.prefix;
    var suffix = numberFormat.suffix;
    var decimalSymbol = numberFormat.decimalSymbol;
    var maximumFractionDigits = numberFormat.maximumFractionDigits;
    var groupingSymbol = numberFormat.groupingSymbol;
    var decimalSymbolPosition = inputtedValue.indexOf(decimalSymbol) + 1;
    var caretPositionFromLeft = inputtedValue.length - caretPosition;

    if (Math.abs(newValue.length - inputtedValue.length) > 1 && caretPosition <= decimalSymbolPosition) {
      return newValue.indexOf(decimalSymbol) + 1;
    } else if (newValue.substr(caretPosition, 1) === groupingSymbol && count(newValue, groupingSymbol) === count(inputtedValue, groupingSymbol) + 1) {
      return newValue.length - caretPositionFromLeft - 1;
    } else {
      if (!options.autoDecimalMode && decimalSymbolPosition !== 0 && caretPosition > decimalSymbolPosition) {
        if (numberFormat.onlyDigits(inputtedValue.substr(decimalSymbolPosition)).length - 1 === maximumFractionDigits) {
          caretPositionFromLeft -= 1;
        }
      }

      return options.distractionFree.hideCurrencySymbol ? newValue.length - caretPositionFromLeft : Math.max(newValue.length - Math.max(caretPositionFromLeft, suffix.length), prefix.length === 0 ? 0 : prefix.length + 1);
    }
  };

  var getDistractionFreeCaretPosition = function getDistractionFreeCaretPosition(numberFormat, options, value, caretPosition) {
    var result = caretPosition;

    if (options.distractionFree.hideCurrencySymbol) {
      result -= numberFormat.prefix.length;
    }

    if (options.distractionFree.hideGroupingSymbol) {
      result -= count(value.substring(0, caretPosition), numberFormat.groupingSymbol);
    }

    return Math.max(0, result);
  };

  var equal = function equal(a, b) {
    if (a === b) {
      return true;
    }

    if (!a || !b || _typeof(a) !== 'object' || _typeof(b) !== 'object') {
      return false;
    }

    var keys = Object.keys(a);

    if (keys.length !== Object.keys(b).length) {
      return false;
    }

    if (!keys.every(Object.prototype.hasOwnProperty.bind(b))) {
      return false;
    }

    return keys.every(function (key) {
      return equal(a[key], b[key]);
    });
  };

  var DECIMAL_SYMBOLS = [',', '.', '٫'];

  var NumberFormat = function NumberFormat(options) {
    var currency = options.currency;
    var locale = options.locale;
    var precision = options.precision;
    var autoDecimalMode = options.autoDecimalMode;
    var valueAsInteger = options.valueAsInteger;
    var numberFormat = new Intl.NumberFormat(locale, typeof currency === 'string' ? {
      currency: currency,
      style: 'currency'
    } : {
      minimumFractionDigits: 1
    });
    var ps = numberFormat.format(123456);
    this.locale = locale;
    this.currency = currency;
    this.digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(function (i) {
      return i.toLocaleString(locale);
    });
    this.decimalSymbol = count(ps, this.digits[0]) ? ps.substr(ps.indexOf(this.digits[6]) + 1, 1) : undefined;
    this.groupingSymbol = ps.substr(ps.indexOf(this.digits[3]) + 1, 1);
    this.minusSymbol = substringBefore(Number(-1).toLocaleString(locale), this.digits[1]);

    if (this.decimalSymbol === undefined) {
      this.minimumFractionDigits = this.maximumFractionDigits = 0;
    } else if (typeof precision === 'number') {
      this.minimumFractionDigits = this.maximumFractionDigits = precision;
    } else if (_typeof(precision) === 'object' && !autoDecimalMode && !valueAsInteger) {
      this.minimumFractionDigits = precision.min || 0;
      this.maximumFractionDigits = precision.max !== undefined ? precision.max : 20;
    } else if (typeof currency === 'string') {
      this.minimumFractionDigits = numberFormat.resolvedOptions().minimumFractionDigits;
      this.maximumFractionDigits = numberFormat.resolvedOptions().maximumFractionDigits;
    } else {
      this.minimumFractionDigits = this.maximumFractionDigits = 2;
    }

    if (typeof currency === 'string') {
      this.prefix = substringBefore(ps, this.digits[1]);
      this.negativePrefix = substringBefore(numberFormat.format(-1), this.digits[1]);
      this.suffix = ps.substring(ps.lastIndexOf(this.decimalSymbol ? this.digits[0] : this.digits[6]) + 1);
    } else {
      this.prefix = (currency || {}).prefix || '';
      this.negativePrefix = "" + this.minusSymbol + this.prefix;
      this.suffix = (currency || {}).suffix || '';
    }
  };

  NumberFormat.prototype.parse = function parse(str) {
    var negative = this.isNegative(str);
    str = this.normalizeDigits(str);
    str = this.stripCurrencySymbol(str);
    str = this.stripMinusSymbol(str);
    var fraction = this.decimalSymbol ? "(" + escapeRegExp(this.decimalSymbol) + "\\d*)?" : '';
    var match = str.match(new RegExp("^" + this.integerPattern() + fraction + "$"));

    if (match) {
      return Number("" + (negative ? '-' : '') + this.onlyDigits(match[1]) + "." + this.onlyDigits(match[3] || ''));
    }

    return null;
  };

  NumberFormat.prototype.format = function format(number, options) {
    if (options === void 0) options = {
      minimumFractionDigits: this.minimumFractionDigits,
      maximumFractionDigits: this.maximumFractionDigits
    };

    if (typeof this.currency === 'string') {
      return number.toLocaleString(this.locale, Object.assign({}, {
        style: 'currency',
        currency: this.currency
      }, options));
    } else {
      return this.insertCurrencySymbol(Math.abs(number).toLocaleString(this.locale, options), number < 0 || number === 0 && 1 / number < 0);
    }
  };

  NumberFormat.prototype.integerPattern = function integerPattern() {
    return "(0|[1-9]\\d{0,2}(" + escapeRegExp(this.groupingSymbol) + "?\\d{3})*)";
  };

  NumberFormat.prototype.toFraction = function toFraction(str) {
    return "" + this.digits[0] + this.decimalSymbol + this.onlyLocaleDigits(str.substr(1)).substr(0, this.maximumFractionDigits);
  };

  NumberFormat.prototype.isFractionIncomplete = function isFractionIncomplete(str) {
    return !!this.normalizeDigits(str).match(new RegExp("^" + this.integerPattern() + escapeRegExp(this.decimalSymbol) + "$"));
  };

  NumberFormat.prototype.isNegative = function isNegative(str) {
    return startsWith(str, this.negativePrefix) || startsWith(str.replace('-', this.minusSymbol), this.minusSymbol);
  };

  NumberFormat.prototype.insertCurrencySymbol = function insertCurrencySymbol(str, negative) {
    return "" + (negative ? this.negativePrefix : this.prefix) + str + this.suffix;
  };

  NumberFormat.prototype.stripMinusSymbol = function stripMinusSymbol(str) {
    return str.replace('-', this.minusSymbol).replace(this.minusSymbol, '');
  };

  NumberFormat.prototype.stripCurrencySymbol = function stripCurrencySymbol(str) {
    return str.replace(this.negativePrefix, '').replace(this.prefix, '').replace(this.suffix, '');
  };

  NumberFormat.prototype.normalizeDecimalSymbol = function normalizeDecimalSymbol(str, from) {
    var this$1 = this;
    DECIMAL_SYMBOLS.forEach(function (s) {
      str = str.substr(0, from) + str.substr(from).replace(s, this$1.decimalSymbol);
    });
    return str;
  };

  NumberFormat.prototype.normalizeDigits = function normalizeDigits(str) {
    if (this.digits[0] !== '0') {
      this.digits.forEach(function (digit, index) {
        str = str.replace(new RegExp(digit, 'g'), index);
      });
    }

    return str;
  };

  NumberFormat.prototype.onlyDigits = function onlyDigits(str) {
    return this.normalizeDigits(str).replace(/\D+/g, '');
  };

  NumberFormat.prototype.onlyLocaleDigits = function onlyLocaleDigits(str) {
    return str.replace(new RegExp("[^" + this.digits.join('') + "]*", 'g'), '');
  };

  var DefaultNumberMask = function DefaultNumberMask(numberFormat) {
    this.numberFormat = numberFormat;
  };

  DefaultNumberMask.prototype.conformToMask = function conformToMask(str, previousConformedValue) {
    var this$1 = this;
    if (previousConformedValue === void 0) previousConformedValue = '';
    var negative = this.numberFormat.isNegative(str);

    var checkIncompleteValue = function checkIncompleteValue(str) {
      if (str === '' && negative && previousConformedValue !== this$1.numberFormat.negativePrefix) {
        return '';
      } else if (this$1.numberFormat.maximumFractionDigits > 0) {
        if (this$1.numberFormat.isFractionIncomplete(str)) {
          return str;
        } else if (startsWith(str, this$1.numberFormat.decimalSymbol)) {
          return this$1.numberFormat.toFraction(str);
        }
      }

      return null;
    };

    var value = str;
    value = this.numberFormat.stripCurrencySymbol(value);
    value = this.numberFormat.stripMinusSymbol(value);
    var incompleteValue = checkIncompleteValue(value);

    if (incompleteValue != null) {
      return this.numberFormat.insertCurrencySymbol(incompleteValue, negative);
    }

    var ref = value.split(this.numberFormat.decimalSymbol);
    var integer = ref[0];
    var fraction = ref.slice(1);
    var integerDigits = removeLeadingZeros(this.numberFormat.onlyDigits(integer));
    var fractionDigits = this.numberFormat.onlyDigits(fraction.join('')).substr(0, this.numberFormat.maximumFractionDigits);
    var invalidFraction = fraction.length > 0 && fractionDigits.length === 0;
    var invalidNegativeValue = integerDigits === '' && negative && (previousConformedValue === str.slice(0, -1) || previousConformedValue !== this.numberFormat.negativePrefix);

    if (invalidFraction || invalidNegativeValue) {
      return previousConformedValue;
    } else if (integerDigits.match(/\d+/)) {
      return {
        numberValue: Number("" + (negative ? '-' : '') + integerDigits + "." + fractionDigits),
        fractionDigits: fractionDigits
      };
    } else {
      return '';
    }
  };

  var AutoDecimalModeNumberMask = function AutoDecimalModeNumberMask(numberFormat) {
    this.numberFormat = numberFormat;
  };

  AutoDecimalModeNumberMask.prototype.conformToMask = function conformToMask(str) {
    if (str === '') {
      return '';
    }

    var negative = this.numberFormat.isNegative(str);
    var numberValue = this.numberFormat.stripMinusSymbol(str) === '' ? -0 : Number("" + (negative ? '-' : '') + removeLeadingZeros(this.numberFormat.onlyDigits(str))) / Math.pow(10, this.numberFormat.minimumFractionDigits);
    return {
      numberValue: numberValue,
      fractionDigits: numberValue.toFixed(this.numberFormat.minimumFractionDigits).slice(-this.numberFormat.minimumFractionDigits)
    };
  };

  var MAX_SAFE_INTEGER = Math.pow(2, 53) - 1;

  var init = function init(el, optionsFromBinding, ref) {
    var $ci = ref.$ci;
    var inputElement = el.tagName.toLowerCase() === 'input' ? el : el.querySelector('input');

    if (!inputElement) {
      throw new Error('No input element found');
    }

    var options = Object.assign({}, $ci ? $ci.GLOBAL_OPTIONS : DEFAULT_OPTIONS, optionsFromBinding);
    var distractionFree = options.distractionFree;
    var autoDecimalMode = options.autoDecimalMode;
    var valueRange = options.valueRange;

    if (typeof distractionFree === 'boolean') {
      options.distractionFree = {
        hideCurrencySymbol: distractionFree,
        hideNegligibleDecimalDigits: distractionFree,
        hideGroupingSymbol: distractionFree
      };
    }

    if (valueRange) {
      options.valueRange = {
        min: valueRange.min !== undefined ? Math.max(valueRange.min, -MAX_SAFE_INTEGER) : -MAX_SAFE_INTEGER,
        max: valueRange.max !== undefined ? Math.min(valueRange.max, MAX_SAFE_INTEGER) : MAX_SAFE_INTEGER
      };
    } else {
      options.valueRange = {
        min: -MAX_SAFE_INTEGER,
        max: MAX_SAFE_INTEGER
      };
    }

    if (autoDecimalMode) {
      options.distractionFree.hideNegligibleDecimalDigits = false;
      inputElement.setAttribute('inputmode', 'numeric');
    } else {
      inputElement.setAttribute('inputmode', 'decimal');
    }

    var currencyFormat = new NumberFormat(options);
    inputElement.$ci = Object.assign({}, inputElement.$ci || {
      numberValue: null
    }, {
      options: options,
      numberMask: options.autoDecimalMode ? new AutoDecimalModeNumberMask(currencyFormat) : new DefaultNumberMask(currencyFormat),
      currencyFormat: currencyFormat
    });
    return inputElement;
  };

  var triggerEvent = function triggerEvent(el, eventName) {
    var ref = el.$ci;
    var numberValue = ref.numberValue;
    var currencyFormat = ref.currencyFormat;
    var options = ref.options;
    numberValue = toExternalNumberModel(numberValue, options.valueAsInteger, currencyFormat.maximumFractionDigits);
    dispatchEvent$1(el, eventName, {
      numberValue: numberValue
    });
  };

  var applyFixedFractionFormat = function applyFixedFractionFormat(el, value, forcedChange) {
    if (forcedChange === void 0) forcedChange = false;
    var ref = el.$ci;
    var currencyFormat = ref.currencyFormat;
    var options = ref.options;
    var ref$1 = options.valueRange;
    var min = ref$1.min;
    var max = ref$1.max;

    var validateValueRange = function validateValueRange() {
      return Math.min(Math.max(value, min), max);
    };

    format(el, value != null ? currencyFormat.format(validateValueRange()) : null);

    if (value !== el.$ci.numberValue || forcedChange) {
      triggerEvent(el, 'change');
    }
  };

  var updateInputValue = function updateInputValue(el, value, hideNegligibleDecimalDigits) {
    if (value != null) {
      var ref = el.$ci;
      var focus = ref.focus;
      var decimalSymbolInsertedAt = ref.decimalSymbolInsertedAt;
      var options = ref.options;
      var numberMask = ref.numberMask;
      var currencyFormat = ref.currencyFormat;
      var previousConformedValue = ref.previousConformedValue;
      var allowNegative = options.allowNegative;
      var distractionFree = options.distractionFree;

      if (decimalSymbolInsertedAt !== undefined) {
        value = currencyFormat.normalizeDecimalSymbol(value, decimalSymbolInsertedAt);
        el.$ci.decimalSymbolInsertedAt = undefined;
      }

      var conformedValue = numberMask.conformToMask(value, previousConformedValue);
      var formattedValue;

      if (_typeof(conformedValue) === 'object') {
        var numberValue = conformedValue.numberValue;
        var fractionDigits = conformedValue.fractionDigits;
        var maximumFractionDigits = currencyFormat.maximumFractionDigits;
        var minimumFractionDigits = currencyFormat.minimumFractionDigits;

        if (focus) {
          minimumFractionDigits = maximumFractionDigits;
        }

        minimumFractionDigits = hideNegligibleDecimalDigits ? fractionDigits.replace(/0+$/, '').length : Math.min(minimumFractionDigits, fractionDigits.length);
        formattedValue = numberValue > MAX_SAFE_INTEGER ? previousConformedValue : currencyFormat.format(numberValue, {
          useGrouping: !(focus && distractionFree.hideGroupingSymbol),
          minimumFractionDigits: minimumFractionDigits,
          maximumFractionDigits: maximumFractionDigits
        });
      } else {
        formattedValue = conformedValue;
      }

      if (!allowNegative) {
        formattedValue = formattedValue.replace(currencyFormat.negativePrefix, currencyFormat.prefix);
      }

      if (focus && distractionFree.hideCurrencySymbol) {
        formattedValue = formattedValue.replace(currencyFormat.negativePrefix, currencyFormat.minusSymbol).replace(currencyFormat.prefix, '').replace(currencyFormat.suffix, '');
      }

      el.value = formattedValue;
      el.$ci.numberValue = currencyFormat.parse(el.value);
    } else {
      el.value = el.$ci.numberValue = null;
    }

    el.$ci.previousConformedValue = el.value;
  };

  var format = function format(el, value, hideNegligibleDecimalDigits) {
    if (hideNegligibleDecimalDigits === void 0) hideNegligibleDecimalDigits = false;
    updateInputValue(el, value, hideNegligibleDecimalDigits);
    triggerEvent(el, 'input');
  };

  var addEventListener = function addEventListener(el) {
    el.addEventListener('input', function (e) {
      if (!e.detail) {
        var value = el.value;
        var selectionStart = el.selectionStart;
        var el_$ci = el.$ci;
        var currencyFormat = el_$ci.currencyFormat;
        var options = el_$ci.options;
        format(el, value);

        if (el.$ci.focus) {
          setCaretPosition(el, getCaretPositionAfterFormat(el.value, value, selectionStart, currencyFormat, options));
        }
      }
    }, {
      capture: true
    });
    el.addEventListener('keypress', function (e) {
      if (DECIMAL_SYMBOLS.includes(e.key)) {
        el.$ci.decimalSymbolInsertedAt = el.selectionStart;
      }
    });
    el.addEventListener('format', function (e) {
      var ref = el.$ci;
      var currencyFormat = ref.currencyFormat;
      var options = ref.options;
      var numberValue = ref.numberValue;

      var toInternalNumberModel = function toInternalNumberModel(n) {
        return options.valueAsInteger && n != null ? n / Math.pow(10, currencyFormat.maximumFractionDigits) : n;
      };

      var newValue = toInternalNumberModel(e.detail.value);

      if (numberValue !== newValue) {
        applyFixedFractionFormat(el, newValue);
      }
    });
    el.addEventListener('focus', function () {
      el.$ci.focus = true;
      var ref = el.$ci.options.distractionFree;
      var hideCurrencySymbol = ref.hideCurrencySymbol;
      var hideGroupingSymbol = ref.hideGroupingSymbol;
      var hideNegligibleDecimalDigits = ref.hideNegligibleDecimalDigits;

      if (hideCurrencySymbol || hideGroupingSymbol || hideNegligibleDecimalDigits) {
        setTimeout(function () {
          var value = el.value;
          var selectionStart = el.selectionStart;
          var selectionEnd = el.selectionEnd;

          if (value) {
            format(el, value, hideNegligibleDecimalDigits);
          }

          if (Math.abs(selectionStart - selectionEnd) > 0) {
            el.setSelectionRange(0, el.value.length);
          } else {
            setCaretPosition(el, getDistractionFreeCaretPosition(el.$ci.currencyFormat, el.$ci.options, value, selectionStart));
          }
        });
      }
    });
    el.addEventListener('blur', function () {
      el.$ci.focus = false;

      if (el.$ci.numberValue != null) {
        applyFixedFractionFormat(el, el.$ci.numberValue);
      }
    });
    el.addEventListener('change', function (e) {
      if (!e.detail) {
        triggerEvent(el, 'change');
      }
    });
  };

  var directive = {
    bind: function bind(el, ref, ref$1) {
      var value = ref.value;
      var context = ref$1.context;
      var inputElement = init(el, value, context);
      addEventListener(inputElement);
      setValue$1(inputElement, inputElement.$ci.currencyFormat.parse(inputElement.value));
    },
    componentUpdated: function componentUpdated(el, ref, ref$1) {
      var value = ref.value;
      var oldValue = ref.oldValue;
      var context = ref$1.context;

      if (!equal(value, oldValue)) {
        var inputElement = init(el, value, context);
        applyFixedFractionFormat(inputElement, inputElement.$ci.numberValue, true);
      }
    }
  };
  var component = {
    render: function render(h) {
      var this$1 = this;
      return h('input', {
        directives: [{
          name: 'currency',
          value: this.options
        }],
        on: Object.assign({}, this.$listeners, {
          change: function change(e) {
            if (e.detail) {
              this$1.$emit('change', e.detail.numberValue);
            }
          },
          input: function input(e) {
            if (e.detail && this$1.value !== e.detail.numberValue) {
              this$1.$emit('input', e.detail.numberValue);
            }
          }
        })
      });
    },
    directives: {
      currency: directive
    },
    name: 'CurrencyInput',
    props: {
      value: {
        type: Number,
        default: null
      },
      locale: {
        type: String,
        default: undefined
      },
      currency: {
        type: [String, Object],
        default: undefined
      },
      distractionFree: {
        type: [Boolean, Object],
        default: undefined
      },
      precision: {
        type: [Number, Object],
        default: undefined
      },
      autoDecimalMode: {
        type: Boolean,
        default: undefined
      },
      valueAsInteger: {
        type: Boolean,
        default: undefined
      },
      valueRange: {
        type: Object,
        default: undefined
      },
      allowNegative: {
        type: Boolean,
        default: undefined
      }
    },
    mounted: function mounted() {
      this.setValue(this.value);
    },
    computed: {
      options: function options() {
        var this$1 = this;
        var options = Object.assign({}, this.$ci ? this.$ci.GLOBAL_OPTIONS : DEFAULT_OPTIONS);
        Object.keys(DEFAULT_OPTIONS).forEach(function (key) {
          if (this$1[key] !== undefined) {
            options[key] = this$1[key];
          }
        });
        return options;
      }
    },
    watch: {
      value: 'setValue'
    },
    methods: {
      setValue: function setValue$1$1(value) {
        setValue$1(this.$el, value);
      }
    }
  };
  var plugin = {
    install: function install(Vue, ref) {
      if (ref === void 0) ref = {};
      var componentName = ref.componentName;
      if (componentName === void 0) componentName = component.name;
      var directiveName = ref.directiveName;
      if (directiveName === void 0) directiveName = 'currency';
      var globalOptions = ref.globalOptions;
      if (globalOptions === void 0) globalOptions = {};
      Vue.component(componentName, component);
      Vue.directive(directiveName, directive);
      Vue.prototype.$ci = {
        getValue: getValue,
        setValue: setValue$1,
        GLOBAL_OPTIONS: Object.assign({}, DEFAULT_OPTIONS, globalOptions)
      };
    }
  };

  if (typeof window !== 'undefined' && window.Vue) {
    window.Vue.use(plugin);
  }

  var options = {
    locale: undefined,
    currency: undefined,
    decimalLength: 2,
    autoDecimalMode: true,
    min: null,
    max: null,
    defaultValue: 0,
    valueAsInteger: false,
    allowNegative: true
  };

  var script = {
    name: 'VCurrencyField',
    props: {
      value: {
        type: [Number, String],
        default: function _default() {
          return 0;
        }
      },
      locale: {
        type: String,
        default: function _default() {
          return options.locale;
        }
      },
      currency: {
        type: [String, Object],
        default: function _default() {
          return options.currency;
        }
      },
      decimalLength: {
        type: [Number, Object],
        default: function _default() {
          return options.decimalLength;
        }
      },
      autoDecimalMode: {
        type: Boolean,
        default: function _default() {
          return options.autoDecimalMode;
        }
      },
      min: {
        type: Number,
        default: function _default() {
          return options.min;
        }
      },
      max: {
        type: Number,
        default: function _default() {
          return options.max;
        }
      },
      defaultValue: {
        type: Number,
        default: function _default() {
          return options.defaultValue;
        }
      },
      valueAsInteger: {
        type: Boolean,
        default: function _default() {
          return options.valueAsInteger;
        }
      },
      allowNegative: {
        type: Boolean,
        default: function _default() {
          return options.allowNegative;
        }
      }
    },
    directives: {
      CurrencyDirective: directive
    },
    data: function data() {
      return {
        formattedValue: this.value
      };
    },
    mounted: function mounted() {
      this.addListeners(this.$el.querySelector('input'));
    },
    computed: {
      attrs: function attrs() {
        // eslint-disable-next-line
        var _this$$attrs = this.$attrs,
            value = _this$$attrs.value,
            attrs = _objectWithoutProperties(_this$$attrs, ["value"]); // all but input event


        return attrs;
      },
      distractionFree: function distractionFree() {
        if (this.decimalLength > 0) {
          return !this.autoDecimalMode;
        } else {
          return false;
        }
      },
      decimalMode: function decimalMode() {
        if (this.decimalLength > 0) {
          return this.autoDecimalMode;
        } else {
          return false;
        }
      },
      valueRange: function valueRange() {
        if (this.min || this.max) {
          return {
            min: this.min,
            max: this.max
          };
        } else {
          return undefined;
        }
      }
    },
    watch: {
      value: 'setValue'
    },
    methods: {
      addListeners: function addListeners(el) {
        var _this = this;

        el.addEventListener('change', function (e) {
          if (e.detail) {
            _this.$emit('change', e.detail.numberValue);
          }

          if (_this.value == null && _this.value == undefined && _this.defaultValue !== null && _this.defaultValue !== undefined) {
            _this.setValue(_this.valueAsInteger && _this.defaultValue ? _this.defaultValue * Math.pow(10, _this.decimalLength) : _this.defaultValue);
          }
        }, {
          capture: true
        });
        el.addEventListener('input', function (e) {
          if (e.detail && _this.value !== e.detail.numberValue) {
            _this.$emit('input', e.detail.numberValue);
          }
        }, {
          capture: true
        });
      },
      setValue: function setValue$1(value) {
        var input = this.$el.querySelector('input');

        setValue(input, value);
      },
      listeners: function listeners() {
        var _this2 = this;

        // eslint-disable-next-line
        var _this$$listeners = this.$listeners,
            input = _this$$listeners.input,
            _keyup = _this$$listeners.keyup,
            listeners = _objectWithoutProperties(_this$$listeners, ["input", "keyup"]); // all but input event


        return _objectSpread2(_objectSpread2({}, listeners), {}, {
          input: function input(value) {
            if (_this2.$refs.textfield.isResetting || value == null) {
              _this2.setValue(_this2.valueAsInteger && _this2.defaultValue ? _this2.defaultValue * Math.pow(10, _this2.decimalLength) : _this2.defaultValue);
            }
          },
          'keyup': function keyup(event) {
            if (event.key === '-' || event.key === '+') {
              if (_this2.value != null && event.key === '-' && _this2.value >= 0) {
                _this2.setValue(_this2.value * -1);
              }

              if (_this2.value != null && event.key === '+' && _this2.value <= 0) {
                _this2.setValue(_this2.value * -1);
              }
            }

            if (_keyup) {
              _keyup();
            }
          }
        });
      }
    }
  };

  function normalizeComponent(template, style, script, scopeId, isFunctionalTemplate, moduleIdentifier
  /* server only */
  , shadowMode, createInjector, createInjectorSSR, createInjectorShadow) {
    if (typeof shadowMode !== 'boolean') {
      createInjectorSSR = createInjector;
      createInjector = shadowMode;
      shadowMode = false;
    } // Vue.extend constructor export interop.


    var options = typeof script === 'function' ? script.options : script; // render functions

    if (template && template.render) {
      options.render = template.render;
      options.staticRenderFns = template.staticRenderFns;
      options._compiled = true; // functional template

      if (isFunctionalTemplate) {
        options.functional = true;
      }
    } // scopedId


    if (scopeId) {
      options._scopeId = scopeId;
    }

    var hook;

    if (moduleIdentifier) {
      // server build
      hook = function hook(context) {
        // 2.3 injection
        context = context || // cached call
        this.$vnode && this.$vnode.ssrContext || // stateful
        this.parent && this.parent.$vnode && this.parent.$vnode.ssrContext; // functional
        // 2.2 with runInNewContext: true

        if (!context && typeof __VUE_SSR_CONTEXT__ !== 'undefined') {
          context = __VUE_SSR_CONTEXT__;
        } // inject component styles


        if (style) {
          style.call(this, createInjectorSSR(context));
        } // register component module identifier for async chunk inference


        if (context && context._registeredComponents) {
          context._registeredComponents.add(moduleIdentifier);
        }
      }; // used by ssr in case component is cached and beforeCreate
      // never gets called


      options._ssrRegister = hook;
    } else if (style) {
      hook = shadowMode ? function () {
        style.call(this, createInjectorShadow(this.$root.$options.shadowRoot));
      } : function (context) {
        style.call(this, createInjector(context));
      };
    }

    if (hook) {
      if (options.functional) {
        // register for functional component in vue file
        var originalRender = options.render;

        options.render = function renderWithStyleInjection(h, context) {
          hook.call(context);
          return originalRender(h, context);
        };
      } else {
        // inject component registration as beforeCreate hook
        var existing = options.beforeCreate;
        options.beforeCreate = existing ? [].concat(existing, hook) : [hook];
      }
    }

    return script;
  }

  var normalizeComponent_1 = normalizeComponent;

  /* script */
  const __vue_script__ = script;

  /* template */
  var __vue_render__ = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('v-text-field',_vm._g(_vm._b({directives:[{name:"currency-directive",rawName:"v-currency-directive",value:({currency: _vm.currency, locale: _vm.locale, distractionFree: _vm.distractionFree, precision: _vm.decimalLength, autoDecimalMode: _vm.decimalMode, valueRange: _vm.valueRange, allowNegative: _vm.allowNegative, valueAsInteger: _vm.valueAsInteger}),expression:"{currency, locale, distractionFree, precision: decimalLength, autoDecimalMode: decimalMode, valueRange, allowNegative, valueAsInteger}"}],ref:"textfield",attrs:{"type":"text"},scopedSlots:_vm._u([_vm._l((_vm.$slots),function(index,name){return {key:name,fn:function(){return [_vm._t(name)]},proxy:true}})],null,true),model:{value:(_vm.formattedValue),callback:function ($$v) {_vm.formattedValue=$$v;},expression:"formattedValue"}},'v-text-field',_vm.attrs,false),_vm.listeners()))};
  var __vue_staticRenderFns__ = [];

    /* style */
    const __vue_inject_styles__ = undefined;
    /* scoped */
    const __vue_scope_id__ = undefined;
    /* module identifier */
    const __vue_module_identifier__ = undefined;
    /* functional template */
    const __vue_is_functional_template__ = false;
    /* style inject */
    
    /* style inject SSR */
    

    
    var VCurrencyField = normalizeComponent_1(
      { render: __vue_render__, staticRenderFns: __vue_staticRenderFns__ },
      __vue_inject_styles__,
      __vue_script__,
      __vue_scope_id__,
      __vue_is_functional_template__,
      __vue_module_identifier__,
      undefined,
      undefined
    );

  var version = '3.1.1';

  function install(Vue, globalOptions) {
    if (globalOptions) {
      Object.keys(globalOptions).map(function (key) {
        options[key] = globalOptions[key];
      });
    }

    Vue.component('v-currency-field', VCurrencyField);
  }

  if (typeof window !== 'undefined' && window.Vue) {
    window.Vue.use(install);
  }

  exports.VCurrencyField = VCurrencyField;
  exports.default = install;
  exports.options = options;
  exports.version = version;

  Object.defineProperty(exports, '__esModule', { value: true });

})));
