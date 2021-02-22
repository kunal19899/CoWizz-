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