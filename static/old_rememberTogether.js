$(function(){
    
    alert("CONNECTED to static/rememberTogether.js!");
    
    let fnames=[];
    let lnames=[];
    let wholeNames=[];
    let nameObjects = [];
    

    getDeparted();
    
    $("#departed-search-btn").on('click',()=>{
        // departed_id = document.getElementById("departed-search-btn").value;
        departed_id = $("#departed-search").val();
        // console.log("DEPARTED id:", departed_id)
        url=`http://127.0.0.1:5000/memorial/${departed_id}`;
        window.location.href = url;
    })

    //get departed - collects all departed in db and formats it for search box
    async function getDeparted() {
        /** GET ALL DEPARTED LIST FROM API then UPDATE DOM */
        let res = await axios.get('/api/departed');
    
        let arrayOfDeparted = res.data.departed;

        
        // ***REMEMBER use for OF not for IN!!! ***
        // let txt=""
        for (friend of arrayOfDeparted) {
            // txt+= build__4_dom(friend);
            fnames.push(friend.fname);
            lnames.push(friend.lname);
            wholeNames.push(`${friend.fname} ${friend.lname}`);
            let wholeName=`${friend.fname} ${friend.lname}`;

            born = makePrettyDate(friend.born);
            died = makePrettyDate(friend.died);
            
            let departedDetail=`${friend.fname} ${friend.lname} (${born} - ${died})`;
            console.log(`${friend.city_born}, ${friend.state_born}`)
                if ((friend.city_born) && (friend.state_born)){
                    departedDetail += `  Born in ${friend.city_born}, ${friend.state_born}`
                };
            departedDetail += ` Memorial id: ${friend.id}`;
            nameObjects.push({label:departedDetail , value:friend.id, id:friend.id});
        }

        for (mem_id of arrayOfDeparted){
            let mem_name = `${mem_id.id}: ${mem_id.fname} ${mem_id.lname}`
            nameObjects.push({label: mem_name, value:mem_id.id, id:friend.id});
        }
        //TODO: ADD ERROR MESSAGES IF NOT FOUND
        //TODO: refactor to get rid of unused

        // TODO: $('.departed-display').append(txt);
        
    }

    //AUTO-FILL
      $( "#departed-search" ).autocomplete({
        source: nameObjects,
        autoFocus: true
        // minLength: 3
      });

    //   $( "#last-names" ).autocomplete({  
    //     source: lnames
    //   });



    function makePrettyDate(date){
        let months =['January','February','March','April','May','June','July','August','September','October','November','December'];

        let dateObj = new Date(date);
        return `${months[dateObj.getMonth()]} ${dateObj.getDate()}, ${dateObj.getFullYear()}`
    }

});