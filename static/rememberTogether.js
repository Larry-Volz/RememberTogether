$(function(){
    
    let fnames=[];
    let lnames=[];
    let wholeNames=[];

    getDeparted();

    //get departed (from cupcakes)
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
            wholeNames.push(`${friend.fname} ${friend.lname}`)
            
        }
        
        // $('.departed-display').append(txt);
        
    }

    //AUTO-FILL
      $( "#first-names" ).autocomplete({
        source: wholeNames
      });

    //   $( "#last-names" ).autocomplete({  
    //     source: lnames
    //   });



});