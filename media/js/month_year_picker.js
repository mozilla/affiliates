(function($) {
    'use strict';

    function MonthYearPicker(selector, options){
        var self = this;
        if (options === undefined) {
            options = {};
        }

        var $picker = $(selector);
        this.$picker = $picker;

        if ($picker.length > 0) {
            this.shortMonthNames = $picker.data('short-month-names');
            this.longMonthNames = $picker.data('long-month-names');
            this.csrf = $picker.data('csrf');
            this.url = options.url || $picker.data('url');

            var date = new Date();
            this.month = options.month || date.getMonth() + 1;
            this.year = options.year || date.getFullYear();

            // Auto-hide so error message stays for non-JS users.
            this.$errorMsg = $(options.errorMsgSelector).hide();

            this.callbacks = [];

            // Bind click events to various elements of the widget.
            var clickEvents = {
                '.picker-header .prev-month': 'evtPrevMonth',
                '.picker-header .current-month-year': 'evtToggleCalendar',
                '.picker-header .next-month': 'evtNextMonth',
                '.year-picker .prev-year': 'evtPrevYear',
                '.year-picker .next-year': 'evtNextYear',
                '.month-picker ul li a': 'evtSelectMonth'
            };
            for (var sel in clickEvents) {
                if (clickEvents.hasOwnProperty(sel)) {
                    // Construct an event handler that will call the event
                    // specified by the property.
                    $(sel).click(this._buildEventHandler(clickEvents[sel]));
                }
            }

            // Special case event: Hide month list on outside click.
            var evtHideMonthList = function evtHideMonthList(e) {
                if (self.$picker.find(e.target).length === 0) {
                    self.$picker.removeClass('opened')
                        .find('.month-picker').hide();
                }
            };
            $(document).on('click', evtHideMonthList);

            this.refresh();
        }
    }

    MonthYearPicker.prototype = {
        _buildEventHandler: function _buildEventHandler(handlerName) {
            var self = this;
            return function(e) {
                e.preventDefault();
                self[handlerName](e);
            };
        },

        evtPrevMonth: function evtPrevMonth() {
            this.month--;
            if (this.month < 1) {
                this.month = 12;
                this.year--;
            }
            this.refresh();
        },
        evtNextMonth: function evtNextMonth() {
            this.month++;
            if (this.month > 12) {
                this.month = 1;
                this.year++;
            }
            this.refresh();
        },
        evtToggleCalendar: function evtToggleCalendar() {
            this.$picker.toggleClass('opened').
                 find('.month-picker').toggle();
        },
        evtPrevYear: function evtPrevYear() {
            this.year--;
            this.refresh();
        },
        evtNextYear: function evtNextYear() {
            this.year++;
            this.refresh();
        },
        evtSelectMonth: function evtSelectMonth(e) {
            this.month = $(e.target).data('number');
            this.refresh();
        },

        // Update the widget display, retrieve new data from the server, and
        // trigger all registered callbacks with the new data.
        refresh: function refresh() {
            var self = this;

            this.updateDisplay();
            $.ajax({
                url: this.url,
                type: 'POST',
                data: {
                    year: this.year,
                    month: this.month,
                    csrfmiddlewaretoken: this.csrf
                }
            }).done(function(data) {
                self.$errorMsg.hide();
                for (var k = 0; k < self.callbacks.length; k++) {
                    self.callbacks[k](data);
                }
            }).fail(function() {
                self.$errorMsg.show();
            });
        },
        updateDisplay: function updateDisplay() {
            var $picker = this.$picker;

            // Month-year text
            $picker.find('.month-year').text(
                this.longMonthNames[this.month - 1] + ' ' + this.year);

            // Calendar Year
            $picker.find('.current-year').text(this.year);

            // Highlighted month.
            $picker.find('.month-number').removeClass('current-month');
            $picker.find('.month-' + this.month).addClass('current-month');
        },

        onRefresh: function onRefresh(callback) {
            this.callbacks.push(callback);
        }
    };

    window.MonthYearPicker = MonthYearPicker;
})(jQuery);