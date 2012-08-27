/**
 * Month Picker Class
 */
var MonthPicker = {

    currentMonth: 1,
    currentYear: 2011,
    monthNames:[],
    fullMonthNames: [],
    csrf: '',
    api_url: '',
    opened:false,
    monthList:null,
    warningMsg: null,
    yourDownloads: null,
    avgDownloads: null,
    /**
     * Month Picker Initialization
     */
    init: function(){
        // Load month names
        var picker = $('.month-year-picker');
        if (picker.length > 0) {
            MonthPicker.monthNames = picker.data('short-month-names');
            MonthPicker.fullMonthNames = picker.data('full-month-names');
            MonthPicker.csrf = picker.data('csrf'),
            MonthPicker.api_url = picker.data('url');

            // Cache Elements
            MonthPicker.monthList = $('.month-picker');

            // Set month and year
            var date = new Date();
            MonthPicker.currentMonth = date.getMonth() + 1;
            MonthPicker.currentYear = date.getFullYear();

            MonthPicker.warningMsg = $('.statistics-warning').hide();
            MonthPicker.yourDownloads = $('#your-downloads');
            MonthPicker.avgDownloads = $('#average-downloads');

            MonthPicker.refresh();
            MonthPicker.addEventListeners();
        }
    },

    addEventListeners: function(){
        var monthPicker = $('.month-year-picker');
        if (monthPicker.length === 0){ return; }

        $('.picker-header .prev-month').click(function(e){
            e.preventDefault();
            MonthPicker.prevMonth();
        });

        $('.picker-header .current-month-year').click(function(e){
            e.preventDefault();
            if (MonthPicker.opened){
                MonthPicker.close();
            } else {
                MonthPicker.open();
            }
        });

        $('.picker-header .next-month').click(function(e){
            e.preventDefault();
            MonthPicker.nextMonth();
        });

        $('.year-picker .prev-year').click(function(e){
            e.preventDefault();
            MonthPicker.currentYear--;
            MonthPicker.refresh();
        });

        $('.year-picker .next-year').click(function(e){
            e.preventDefault();
            MonthPicker.currentYear++;
            MonthPicker.refresh();
        });

        $('.month-picker ul li a').click(function(e){
            e.preventDefault();
            MonthPicker.currentMonth = $(this).data('number');
            MonthPicker.refresh();
        });

        $('.month-year-picker').mouseleave(function(){
            setTimeout(function(){
                MonthPicker.close();
            },200);
        });

    },
    refresh:function(){
        // set month-year
        $('.month-year-picker .month-year').html(
            MonthPicker.fullMonthNames[MonthPicker.currentMonth - 1] + ' ' +
                MonthPicker.currentYear
        );

        // set year
        $('.month-picker .current-year').html(MonthPicker.currentYear);

        // set month
        $('.month-year-picker ul li').removeClass('current-month');
        $.each($('.month-picker ul li'),function(i,val){
            if ( (i+1) == MonthPicker.currentMonth){
                $(this).addClass('current-month');
            }
        });
        MonthPicker.getData();
    },
    open:function(){
        MonthPicker.monthList.show();
        MonthPicker.opened = true;
        $('.current-month-year').css('background-color','#e8f2ff');
    },
    close:function(){
        MonthPicker.monthList.hide();
        MonthPicker.opened = false;
        $('.current-month-year').css('background-color','#FFF');
    },
    nextMonth:function(){
        if (MonthPicker.currentMonth < 12){
            MonthPicker.currentMonth++;
        }else{
            MonthPicker.currentMonth = 1;
            MonthPicker.currentYear++;
        }
        MonthPicker.refresh();
    },
    prevMonth:function(){
        if (MonthPicker.currentMonth > 1){
            MonthPicker.currentMonth--;
        }else{
            MonthPicker.currentMonth = 12;
            MonthPicker.currentYear--;
        }
        MonthPicker.refresh();
    },
    getData:function(){
        // MonthPicker.currentMonth [int 1-12]
        // MonthPicker.currentYear [int]
        $.ajax({
            url: MonthPicker.api_url,
            data: {
                year: MonthPicker.currentYear,
                month: MonthPicker.currentMonth,
                csrfmiddlewaretoken: MonthPicker.csrf
            },
            type: 'POST',
            success: function(data) {
                MonthPicker.warningMsg.hide();
                MonthPicker.yourDownloads.text(data['user_total']);
                MonthPicker.avgDownloads.text(data['site_avg']);
            },
            error: function() {
                MonthPicker.warningMsg.show();
            }
        });
    }
};