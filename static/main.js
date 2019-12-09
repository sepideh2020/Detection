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
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
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

                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                data = data.replace("]","")
                data = data.replace("[","")
                data = data.replace("'","")
                data = data.replace(" ","")
                data = data.split(",")

                $('#result0').html("Angry" + data[0])
                $('#result1').html(" Disgust/fear/surprise" + data[1])
                $('#result2').html(" Sad" + data[2])
                $('#result3').html("Happy" + data[3])
                $('#result4').html("Neutral" + data[4])
                urlOfImg = data.pop()
                console.log(data)
                data = data.map(Number);
                console.log(data)
                var indexOfMaxValue = arrayMaxIndex(data)
                console.log(indexOfMaxValue);
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
                $('#imagePreview').html('<img src="/static/images/' + urlOfImg.replace(/\s+/g, '').replace("'","") + '"/>')
                $('#result5').html(state)

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
