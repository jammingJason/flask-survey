startSurvey = document.querySelector('#btnStart')
startSurvey.addEventListener('click', function(evt){
    evt.preventDefault()
    document.location = '/question/0'
})