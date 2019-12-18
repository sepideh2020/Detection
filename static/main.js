$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('box').html('    <div class="image-section" style="display:none;"><div class="img-preview holder"><div id="imagePreview"></div></div><div><div  id="imgPre"></div>     <button type="button" class="btn btn-primary btn-lg " id="btn-predict">Predict!</button>  </div>    </div>')
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
                $('.imHidden').removeClass('imHidden').addClass('holder');

            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });
var arrayMaxIndex = function(array) {
  return array.indexOf(Math.max.apply(null, array));
};
    $('')
    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,

            processData: false,
            async: true,
            success: function (data) {
                data = data.replace('\"',"")
                data = data.replace("]","")



                data = data.split("]").join("");
                data = data.split("[").join("");
                data = data.split("'").join("");
                data = data.split("  ").join(" ");


                data = data.split(',')
                n = parseInt(data[0]) - 1
                urlOfI = data[n]
                console.log(data)

                imgUrl = data.pop()
                data.shift()
                console.log(data)
                console.log("ASds")
                console.log(n)
      retStr = "status:  "
      listOfPerson = []
                sadasd = []
                for (i = 0; i < n ; i++) {
                  splited = data[i].trim().split(" ")
//                  splited.shift()                splited.pop()

                    map1 = splited.map(x => Number(x * 100))
                    sadasd = map1
                    listOfPerson.push(sadasd)
                    var indexOfMaxValue = arrayMaxIndex(map1)
                    console.log(indexOfMaxValue)

                    console.log(map1)


                    var state = "UnKnown"
                 switch(indexOfMaxValue) {
                      case 0:
                        state = " Angry"
                        break;
                      case 1:
                        state = " Disgust/fear/surprise"
                        break;
                      case 2:
                        state = "Sad"
                        break;
                      case 3:
                        state = "Happy"
                        break;
                      default:
                      state = "Neutral"
                        break;
                    }
                    retStr = retStr.concat("the person Number ", i, " is ", state , " ")

                }



console.log(listOfPerson)

                    infoList = []
                    console.log(n)
                    console.log("This is N")

                    switch(n) {
                      case 1:
                        infoList =  [
                            {
                            label: 'Pesron 1',
                            data: [{x: 1, y: listOfPerson[0][0]}, {x: 2, y: listOfPerson[0][1]}, {x: 3, y: listOfPerson[0][2]},{x: 4, y: listOfPerson[0][3]},{x: 4, y: listOfPerson[0][4]}],
                            showLine: true,
                            fill: false,
                            borderColor: 'rgba(0, 200, 0, 1)'
                            }
                        ]
                        break;
                      case 2:
                    infoList =  [
                            {
                            label: 'Pesron 1',
                            data: [{x: 1, y: listOfPerson[0][0]}, {x: 2, y: listOfPerson[0][1]}, {x: 3, y: listOfPerson[0][2]},{x: 4, y: listOfPerson[0][3]},{x: 4, y: listOfPerson[0][4]}],
                            showLine: true,
                            fill: false,
                            borderColor: 'rgba(134, 100, 0, 1)'
                            },
                            {
                            label: 'Person 2',
                            data: [{x: 1, y: listOfPerson[1][0]}, {x: 2, y: listOfPerson[1][1]}, {x: 3, y: listOfPerson[1][2]},{x: 4, y: listOfPerson[1][3]},{x: 4, y: listOfPerson[1][4]}],
                            showLine: true,
                            fill: false,
                            borderColor: 'rgba(0, 200, 0, 1)'
                            }
                        ]
                        break;
                      case 3:
                            infoList =  [
                            {
                            label: 'Pesron 1',
                            data: [{x: 1, y: listOfPerson[0][0]}, {x: 2, y: listOfPerson[0][1]}, {x: 3, y: listOfPerson[0][2]},{x: 4, y: listOfPerson[0][3]},{x: 4, y: listOfPerson[0][4]}],
                            showLine: true,
                            fill: false,
                            borderColor: 'rgba(134, 100, 0, 1)'
                            },
                            {
                            label: 'Person 2',
                            data: [{x: 1, y: listOfPerson[1][0]}, {x: 2, y: listOfPerson[1][1]}, {x: 3, y: listOfPerson[1][2]},{x: 4, y: listOfPerson[1][3]},{x: 4, y: listOfPerson[1][4]}],
                            showLine: true,
                            fill: false,
                            borderColor: 'rgba(0, 200, 0, 1)'
                            },
                            {
                            label: 'Person 3',
                            data: [{x: 1, y: listOfPerson[2][0]}, {x: 2, y: listOfPerson[2][1]}, {x: 3, y: listOfPerson[2][2]},{x: 4, y: listOfPerson[2][3]},{x: 4, y: listOfPerson[2][4]}],
                            showLine: true,
                            fill: false,
                            borderColor: 'rgba(87, 32, 76, 1)'
                            }
                        ]
                        break;
                      case 3:
                        state = "Happy"
                        break;
                      default:
                      state = "Neutral"
                        break;
                    }





                    console.log(retStr)

          // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);

                $('#imagePreview').fadeOut(650);

                $('#result0').html(retStr)
//                $('#result1').html(" Disgust/fear/surprise" + data[1])
//                $('#result2').html(" Sad" + data[2])
//                $('#result3').html("Happy" + data[3])
//                $('#result4').html("Neutral" + data[4])
                $('.holder').removeClass('holder').addClass('imHidden');


                 urlOfI = urlOfI.split(" ").join("");
                $('#imgPre').html('<img src="/static/images/' + imgUrl.trim() + '"/>')
//                $('#result5').html(state)

   var ctx = document.getElementById('myChart').getContext('2d');
   var chart = new Chart(ctx, {  type: 'scatter',


    // The data for our dataset
    data: {
        labels: ['Angry', 'Disgust/fear/Suprise', 'Sad', 'Happy', 'Neutral'],
        datasets: infoList
    },

    // Configuration options go here
    options: {}
});

            },
             error: function(xhr, textStatus, error) {
                    console.log(xhr.responseText);
                    console.log(xhr.statusText);
                    console.log(textStatus);
                    console.log(error);

                  }
        });
    });

});
