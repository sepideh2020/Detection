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
                n = parseInt(data[0])
                urlOfI = data[n]

      retStr = "status:  "
                sadasd = []
                for (i = 1; i < n ; i++) {
                  splited = data[i].split(" ")
                  splited.pop()
                  splited.shift()
                    map1 = splited.map(x => Number(x * 100))
                    sadasd = map1
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
                $('#imgPre').html('<img src="/static/images/' + urlOfI + '"/>')
//                $('#result5').html(state)

   var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['Angry', 'Disgust', 'Sad', 'Happy', 'Neutral'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [map1[0],map1[1],map1[2],map1[3]]
        }]
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
