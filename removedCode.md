########### input bar ##############

<form action="animate" method="POST" novalidate></form>
                        <div name="states" class="dropdown m-2">
                            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                                Select upto 5 states...
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton1" >
                              
                                {% for state in states.keys() %}

                                <input name="{{state}}" class="m-1" type="checkbox" value="{{states[state]}}">{{state}}<br/>

                                {% endfor %}

                            </div>
                        </div>
                        
                        <select id="feature1" class="card btn btn-light m-2" name="feature1">
                            <option value="">1</option>
                            <option value="">2</option>
                            <option value="">3</option>
                        </select>

                        <select id="feature2" class="card btn btn-light m-2" name="feature1">
                            <option value="">1</option>
                            <option value="">2</option>
                            <option value="">3</option>
                        </select>

                        
                        <input id="submit" class="btn btn-light m-2" type="submit" value ="Submit">
                    </form>



######## map function ######

@app.route("/map", methods=['GET','POST'])
def map():
    correctInput = True
    inputForm = InputForm()
    message = ''
    highlights=''

    if request.method == "POST":
        ipt = request.form
        periodLength = ipt['periodLength']
        start_of_startDate = ipt['start_of_startDate']
        
        start_of_endDate = ipt['start_of_endDate']

        interval = ipt['interval']

        start_of_startDate = datetime.strptime(start_of_startDate, '%Y-%m-%d')
        end_of_startDate = start_of_startDate.date() + timedelta(days=int(periodLength)-1)
        

        start_of_endDate = datetime.strptime(start_of_endDate, '%Y-%m-%d')
        end_of_endDate = start_of_endDate.date() + timedelta(days=int(periodLength)-1)
  
	
    articles = ArticleSearch(start_of_endDate.date(), end_of_endDate)
    highlights = articles.search()	

    end_of_startDate_strip = str(end_of_startDate).split('-')

    x = datetime(int(end_of_startDate_strip[0]), int(end_of_startDate_strip[1]), int(end_of_startDate_strip[2]))
    end_of_startDate = x.strftime("%d-%b-%Y")

    end_of_endDate_strip = str(end_of_endDate).split('-')
    x = datetime(int(end_of_endDate_strip[0]), int(end_of_endDate_strip[1]), int(end_of_endDate_strip[2]))
    end_of_endDate = x.strftime("%d-%b-%Y")


    start_of_startDate_strip = str(start_of_startDate.date()).split('-')
    x = datetime(int(start_of_startDate_strip[0]), int(start_of_startDate_strip[1]), int(start_of_startDate_strip[2]))
    start_of_startDate = x.strftime("%d-%b-%y").upper()

    start_of_endDate_strip = str(start_of_endDate.date()).split('-')
    x = datetime(int(start_of_endDate_strip[0]), int(start_of_endDate_strip[1]), int(start_of_endDate_strip[2]))
    start_of_endDate = x.strftime("%d-%b-%y").upper()

    endDates = {
        'start': end_of_startDate,
        'end': end_of_endDate
    }
    
    gen_map = map_test(periodLength, start_of_startDate, start_of_endDate, interval)
    key = gen_map.main()
    maphash = gen_map.get_maphash()
    returned_map = maphash[key]
    filepath = "maps/Cases-" + start_of_startDate + "vs" + start_of_endDate + "-intDays" + periodLength + "/" + returned_map
    
    check_return_to_default()
    if endDates['start']:
        return render_template("index.html", form = inputForm, message = message, intervals=intervals, rates=rates, check=check, filepath=filepath, highlights=highlights, ipt=ipt, start = endDates['start'], end=endDates['end'])


rates = {
    0: 'Severity Rate',
    1: 'Big Dip',
    2: 'Downtick',
    3: 'Decrease',
    4: 'Flat',
    5: 'Increase',
    6: 'Uptick',
    7: 'Spike',
    8: 'All',
}

intervals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]



check = {
    'period': 1,
    'startDate': 1,
    'endDate': 1,
    'interval': 1,
}

# helper function beyond this point
def check_return_to_default():
    check['period'] = 1
    check['startDate'] = 1
    check['endDate'] = 1
    check['interval'] = 1

{% if link %}

            <div class="embed-responsive embed-responsive-21by9 text-center m-1 " style="">
                <iframe src="" width="100%;" class="embed-responsive-item" allowfullscreen></iframe>
            </div>

            {% else %}

            <div class="embed-responsive embed-responsive-16by9 text-center m-1 bg-dark" style="">
                Hello
                <iframe src="{{ url_for('static', filename='animations/graphtest.html') }}" width="100%;" class="embed-responsive-item" allowfullscreen></iframe>
            </div>

            {% endif %}




            function toBorderDark(id){
                document.getElementById(id).classList.remove('border-danger');
            }

            function adjust_min_of_2nd_period(){
                if ((document.getElementById('start_of_startDate').value != '')){
                    var vals = document.getElementById('start_of_startDate').value.split('-');
                    var year = vals[0];
                    var month = vals[1];
                    var day = vals[2];
                    var date = new Date(year, month-1, day);
                    date.setDate(date.getDate() + parseInt(document.getElementById('periodLength').value));
                    var month = parseInt(date.getMonth())+1
                    if (month < 10){
                        month = 0+month.toString();
                    }
                    var exactDate = date.getDate();
                    if (exactDate < 10){
                        exactDate = 0+exactDate.toString();
                    }
                    var x = document.getElementById('start_of_endDate').min = date.getFullYear() + "-" + month + "-" + exactDate;
                }
            }
            
            function monthName(m){
                if (m == '01')
                    return "Jan";
                if (m == '02')
                    return "Feb";
                if (m == '03')
                    return "Mar";
                if (m == '04')
                    return "Apr";
                if (m == '05')
                    return "May";
                if (m == '06')
                    return "Jun";
                if (m == '07')
                    return "Jul";
                if (m == '08')
                    return "Aug";
                if (m == '09')
                    return "Sep";
                if (m == '10')
                    return "Oct";
                if (m == '11')
                    return "Nov";
                if (m == '12'){
                    return "Dec";
                }
                if (m == 'Jan'){
                    return "01";
                }
                if (m == 'Feb'){
                    return "02";
                }
                if (m == 'Mar'){
                    return "03";
                }
                if (m=="Apr"){
                    return "04";
                }
                if (m=="Jun"){
                    return "06";
                }
                if (m=='Jul'){
                    return "07";
                }
                if (m == 'Aug'){
                    return "08";
                }
                if (m == "Sep"){
                    return "09";
                }
                if (m == "Oct"){
                    return "10";
                }
                if (m == "Nov"){
                    return "11";
                }
                if (m == "Dec"){
                    return "12";
                }
            }

            function set_max_date(){
                // ASantra (12/7): Adjusting based on user's local time
                var now = new Date();
                var utc = new Date(now.getTime() + now.getTimezoneOffset() * 60000);
                var today = new Date(utc.getTime() - 660 * 60000); // converting to current time in CDT (updates at 5am CDT)

                var end = new Date();
                
                end.setDate(today.getDate() - (parseInt(document.getElementById('periodLength').value)));
                var date = end.getFullYear()+'-'+(end.getMonth()+1)+'-'+end.getDate();
                var vals = date.split('-');
                var year = vals[0];
                var month = vals[1];
                var day = vals[2];
                if (month < 10){
                    month = 0+month.toString();
                }
                if (day < 10){
                    day = 0+day.toString();
                }
                var date = year +'-'+ month +'-'+ day;
                var maxEndDate = document.getElementById('start_of_endDate').max = date; 
                
                var start = new Date();
                start.setDate(today.getDate() - 2*(parseInt(document.getElementById('periodLength').value)));
                date = start.getFullYear()+'-'+(start.getMonth()+1)+'-'+start.getDate();
                vals = date.split('-');
                year = vals[0];
                month = vals[1];
                day = vals[2];
                console.log(vals);
                console.log(vals[2]);
                console.log(day);
                if (month < 10){
                    month = 0+month.toString();
                }
                if (day < 10){
                    day = 0+day.toString();
                }
                date = year +'-'+ month +'-'+ day;
                var maxStartDate = document.getElementById('start_of_startDate').max = date;
                console.log(maxStartDate);
            }

            function enable_2nd_calander(){
                if ((document.getElementById('start_of_startDate').value != '') && (document.getElementById('periodLength').value != 0)){
                    document.getElementById('start_of_endDate').disabled = false;
                }

                if ((document.getElementById('periodLength').value == 0) || (document.getElementById('start_of_startDate').value == '')){
                    document.getElementById('start_of_endDate').disabled = true;
                }
            }

            function enable_1st_calander(){
                if (document.getElementById('periodLength').value == 0){
                    document.getElementById('start_of_startDate').disabled = true;
                }
                else{
                    document.getElementById('start_of_startDate').disabled = false;
                }
            }

            function enableSubmit(){
                console.log(document.getElementById('interval').value); 
                if (document.getElementById('periodLength').value == 0){
                    document.getElementById('submit').disabled = true;
                }
                else if((document.getElementById('start_of_startDate').value == '') || (document.getElementById('start_of_endDate').value == '')){
                    document.getElementById('submit').disabled = true;
                }
                else if (document.getElementById('interval').value == 0){
                                   document.getElementById('submit').disabled = true;}
                else {
                    document.getElementById('submit').disabled = false;
                }
            }

            function setEnd(id){
                if (id == 'start_of_startDate'){
                    var vals = document.getElementById('start_of_startDate').value.split('-');
                }
                else if (id == 'start_of_endDate'){
                    var vals = document.getElementById('start_of_endDate').value.split('-');
                    var endOfStart = document.getElementById('end_of_startDate').innerHTML.split('-');
                    // console.log(document.getElementById('end_of_startDate').innerHTML);
                    var endOfStartDate = new Date(endOfStart[2], monthName(endOfStart[1])-1, endOfStart[0]);
                }
                    var year = vals[0];
                    var month = vals[1];
                    var day = vals[2];
                    var date = new Date(year, month-1, day);
                    var dateTemp = new Date(year, month-1, day);

                    // end date 
                    date.setDate(date.getDate() + parseInt(document.getElementById('periodLength').value)-1);
                    var month = parseInt(date.getMonth())+1
                    if (month < 10){
                        month = 0+month.toString();
                    }
                    var exactDate = date.getDate();
                    if (exactDate < 10){
                        exactDate = 0+exactDate.toString();
                    }

                    // ASantra (11/20): check if generated date is >= (INVALID) or < (VALID) compared to today's date
                    // ASantra (12/7): Adjusting based on user's local time
                    var now = new Date();
                    var utc = new Date(now.getTime() + now.getTimezoneOffset() * 60000);
                    var today = new Date(utc.getTime() - 660 * 60000); // converting to current time in CDT

                    // var today = new Date();
                    var todayTemp = new Date(today.getFullYear(), today.getMonth(), today.getDate());

                    if (date>=todayTemp){
                        // Beyond today's date => RESET
                        if (id == 'start_of_startDate'){
                            var x = document.getElementById('start_of_startDate').value = '';
                            var y = document.getElementById('end_of_startDate').innerHTML = '-';
                            enableSubmit(); // new update
                        }
                        else if (id == 'start_of_endDate'){
                            var x = document.getElementById('start_of_endDate').value = '';
                            var y = document.getElementById('end_of_endDate').innerHTML = '-';
                            enableSubmit(); // new update
                        }
                    }
                    else if (id == 'start_of_endDate' && dateTemp <= endOfStartDate){
                            // ASantra (12/2): If the period change leads to a case where start of end date is beyond or equal to the updated end of start date
                            var x = document.getElementById('start_of_endDate').value = '';
                            var y = document.getElementById('end_of_endDate').innerHTML = '-';
                            enableSubmit(); // new update                        
                    }
                    else {
                        // Valid end date => UPDATE
                        if (id == 'start_of_startDate'){
                            var x = document.getElementById('end_of_startDate').innerHTML =  exactDate + "-" + monthName(month) + "-" +date.getFullYear();
                        }
                        else if (id == 'start_of_endDate'){
                            var x = document.getElementById('end_of_endDate').innerHTML = exactDate + "-" + monthName(month) + "-" +date.getFullYear();
                        }    
                    }
                    
                    
                
            }

            function resetDates(id){
                if (id != 'start_of_startDate'){
                    
                    if (id == 'start_of_endDate'){
                        var vals = document.getElementById('end_of_startDate').innerHTML.split('-');
                        var vals_end = document.getElementById('start_of_endDate').value.split('-');

                        var date = new Date(vals[2], parseInt(monthName(vals[1]))-1, vals[0]);
                        var date_end = new Date(vals_end[0], parseInt(vals_end[1])-1, vals_end[2]);

                        if (date >= date_end){
                            var x = document.getElementById('start_of_startDate').value = '';
                            var y = document.getElementById('end_of_startDate').innerHTML = '-';
                            enableSubmit(); // new update
                        }
                    }

                }
                if (id != 'start_of_endDate'){
                    
                    if (id == 'start_of_startDate'){
                        var vals = document.getElementById('end_of_startDate').innerHTML.split('-');
                        var vals_end = document.getElementById('start_of_endDate').value.split('-');

                        var date = new Date(vals[2], parseInt(monthName(vals[1]))-1, vals[0]);
                        var date_end = new Date(vals_end[0], parseInt(vals_end[1])-1, vals_end[2]);

                        if (date >= date_end){
                            var x = document.getElementById('start_of_endDate').value = '';
                            var y = document.getElementById('end_of_endDate').innerHTML = '-';
                            enableSubmit(); // new update
                        }
                    }
                }

                if (id == 'periodLength'){
                       if (document.getElementById('start_of_startDate').value != '')
                            setEnd('start_of_startDate');
                            
                       if (document.getElementById('start_of_endDate').value != '')
                            setEnd('start_of_endDate');   
                }
            }