window.onload = function () {
    var R = Raphael("us-map", 1000, 600),
      attr = {
      "fill": "#d3d3d3",
      "stroke": "#fff",
      "stroke-opacity": "1",
      "stroke-linejoin": "round",
      "stroke-miterlimit": "4",
      "stroke-width": "0.75",
      "stroke-dasharray": "none",
    },
    usRaphael = {};
    
    var curState;
    var prevState;

    // Removes fixed width & height attributes
    // Combine with css width and height of 100% to make map scale to fit its container.
    var svg = document.querySelector("svg");
    svg.removeAttribute("width");
    svg.removeAttribute("height");

    // Resizes viewbox of map with less margin
    R.setViewBox(0,0,925,600,true);

    //Draw Map and store Raphael paths
    for (var state in usMap) {
      usRaphael[state] = R.path(usMap[state]).attr(attr);
    }
    
    //Do Work on Map
    for (var state in usRaphael) {
      usRaphael[state].color = Raphael.getColor();
      
      (function (st, state) {

        st[0].style.cursor = "pointer";

        st[0].onmouseover = function () {
          st.animate({fill: st.color}, 500);
          st.toFront();
          R.safari();
        };

        st[0].onmouseout = function () {
          if (st != curState) {
              st.animate({fill: "#d3d3d3"}, 500);
              st.toFront();
              R.safari();
          }
        };

        st[0].onclick = function () {
          // The attribute names of usRaphael object are not accessible directly,
          // so the below technique gets the attribute name (name of selected state as string)
          // using the keys() method.
          var keys = Object.keys(usRaphael);
          for (i = 0; i < keys.length; i++) {
            if (usRaphael[keys[i]] == st) {
              var myKey = keys[i];
            }
          }
          document.getElementById("state-select").value = myKey;
          console.log(st);
          prevState = curState;
          curState = st;
          prevState.animate({fill: "#d3d3d3"}, 500);
          prevState.toFront();
          curState.animate({fill: st.color}, 500);
          curState.toFront();
          R.safari();
        };

        // Changes the highlighted state when user changes the dropdown selection
        document.getElementById("state-select").onchange = function () {
          prevState = curState;
          curState = usRaphael[document.getElementById("state-select").value];
          prevState.animate({fill: "#d3d3d3"}, 500);
          prevState.toFront();
          curState.animate({fill: curState.color}, 500);
          curState.toFront();
          R.safari();
        };
                   
      })(usRaphael[state], state);
    }
  };