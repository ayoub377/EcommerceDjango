  function addplusminus(e) {

        let fieldname = e.getAttribute("data-field");
        const type = e.getAttribute("data-type");
        let input = document.querySelector("input[name='" + fieldname + "']")
        let currentVal = parseInt(input.value);
          if (!isNaN(currentVal))
          {
    if (type === 'minus') {

      if (currentVal > input.getAttribute('data-min'))
      {
        input.value= (currentVal -1);
      }


    }
     if (type === 'plus')
    {

      if (currentVal < input.getAttribute('data-max')) {
        input.value= (currentVal + 1);
      }

      }

    }

    if(isNaN(currentVal))
    {
        input.value = (currentVal+1);
    }

  }



  function Change(e) {

      let i=0;
      const minValue = parseInt(e.getAttribute('data-min'));
      const maxValue = parseInt(e.getAttribute('data-max'));
      const valueCurrent = parseInt(e.value);
      let preced_value;
      if(isNaN(valueCurrent))
      {

      }

      if (valueCurrent < minValue) {

          alert('desole,vous avez depassez la valeur minimum!');
          e.value = minValue;
      }
      if (valueCurrent >= maxValue) {
          e.value = maxValue;

      }
  }



  function ChangeImg(e)
  {
      let img_center = document.getElementById("img-center");
      let img_second=e;
      let img_center_src = img_center.getAttribute("src");
      let img_second_src = e.getAttribute("src");
      let img_center_data_zoom = img_center.getAttribute("data-zoom-image");
      let img_second_data_zoom = e.getAttribute("data-zoom-image");
      img_center.setAttribute("src",img_second_src);
      img_second.setAttribute("src",img_center_src);
      img_center.setAttribute("data-zoom-image",img_second_data_zoom);
      img_second.setAttribute("data-zoom-image",img_center_data_zoom);

      $('.zoomWindow').css("background-image",`url(${img_second_src})`);

  }

  function StartZoom() {

        $('#img-center').ezPlus({
            lensShape: 'round',
            lensSize: 50
        })
    }

     $(document).ready(function (){
        $('.deals').slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay:true,
            autoplaySpeed:5000,
            responsive:[
                {
                    breakpoint:880,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1,
                        autoplay:true,
                        autoplaySpeed:5000,

                    }

                },
                {
                     breakpoint:670,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        autoplay:true,
                        autoplaySpeed:5000,


                    }
                }


            ]

        })

    })


