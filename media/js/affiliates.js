/**
 * Page Initialization
 */
$(
    function(event){
        MonthPicker.init();
        HomePage.init();
    }
);

/**
 * Home Page Class
 */
var HomePage = {

    /**
     * Home Page Initialization
     */
    init: function(){
        HomePage.addEventListeners();
    },

    /**
     *
     */
    addEventListeners: function(){
        if ($(".js_no_action").length) {
            $(".js_no_action").click(function(e){
                e.preventDefault();
            });
        }
        if ($(".js_accordion").length) {
            $(".js_accordion").each(function(index, elem){
                HomePage.initAccordion(elem);
            });
        }
        if ($(".show_tooltip").length) {
            $(".show_tooltip").click(function(e){
                e.preventDefault();
            });
            $(".show_tooltip").hover(
                function(e){
                    HomePage.toggleToolTip($(this).attr('target'), e.type);
                },
                function(e){
                    HomePage.toggleToolTip($(this).attr('target'), e.type);
                });
        }
        if($.browser.msie) {
            $('input[placeholder], textarea[placeholder]').placeholder();
        }
        if ($(".js_uniform").length) {
            $(".js_uniform").uniform();
        }
    },
    toggleToolTip: function(rel, e){
        var toolTip = $('#'+rel),
            timer;

        if (e == "mouseenter") {
            toolTip.show();
        } else {
            toolTip.hide();
        }
    },
    initAccordion : function(elem){
        var ulAccordion = $(elem),
            lnkAction = $("h5 a", ulAccordion),
            liElement, answerElement;

        ulAccordion.children().removeClass().addClass('collapsed');
        lnkAction.each(function(){
            $(this).click(function(e){
                e.preventDefault();
                liElement = $(this).parents('li');
                answerElement = $('.answer', liElement);
                if (liElement.hasClass('collapsed')) {
                    answerElement.slideDown('fast', function() {
                        liElement.removeClass().addClass('expanded');
                    });
                } else {
                    answerElement.slideUp('fast', function() {
                        liElement.removeClass().addClass('collapsed');
                    });
                }
            });
        });
    }
};
/**
 * Month Picker Class
 */
var MonthPicker = {

    currentMonth: 1,
    currentYear: 2011,
    monthNames:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct',
                'Nov','Dec'],
    fullMonthNames:['January','February','March','April','May','June','July',
                    'August','September','October','November','December'],
    opened:false,
    monthList:null,
    /**
     * Month Picker Initialization
     */
    init: function(){
        MonthPicker.refresh();
        MonthPicker.addEventListeners();
    },

    /**
     *
     */
    addEventListeners: function(){
        var monthPicker = $('.month-year-picker');
        if (monthPicker.length === 0){ return; }

        // Cache Elements
        MonthPicker.monthList = $('.month-picker');

        // set current month
        MonthPicker.currentMonth = parseInt($('.month-picker ul li.current-month a').attr('title'), 10) || 1;

        // set current year
        MonthPicker.currentYear = parseInt($('.month-picker .year-picker .current-year').text(), 10) || 2011;

        // pull month name list from document
        var months = $('.month-picker ul li a');
        if (months.length > 0){
            MonthPicker.monthNames = [];
            $.each($('.month-picker ul li a'),function(i,val){
                MonthPicker.monthNames.push($(this).html());
            });
        }

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
            MonthPicker.currentMonth = parseInt($(this).attr('title'),10);
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
        // ajax call here
        // Params
        // MonthPicker.currentMonth [int 1-12]
        // MonthPicker.currentYear [int]
    }
};
