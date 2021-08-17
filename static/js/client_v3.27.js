$( document ).ready( onReady );

function onReady(){
    console.log( 'in jq');
    getAnimals();
    $( '#animalTables' ).on( 'click', '.removeButton', removeAnimal )
    $( '#animalTables' ).on( 'click', '.editButton', editAnimal )
}

function getAnimals(){
    //call ajax w/GET route
    $.ajax({
        method: 'GET',
        url: '/api/animals'
    }).then( function( response ){
        console.log( 'back from GET with response', response );
        //assign the two table DOM elements to new variables for output
        let el = $( '#animalsOut' );
        let elTwo = $( '#holdingOut' );
        //empty
        el.empty();
        elTwo.empty();
        //loop thru all of the database
        for ( let i=0; i<response.length; i++ ){
            let animal = response[i];
            // let checkMark = `<button data-id="${task.id}" class="checkOffTaskButton">&#10004</button>`;
            // checkMark = `-`
            if ( animal.on_display === true ){
                el.append(`
                <tr data-id=${animal.id}>
                    <td>${animal.id}</td>
                    <td>${animal.species}</td>
                    <td>${animal.age}</td>
                    <td>${animal.gender}</td>
                    <td>${animal.name}</td>
                    <td>${animal.exhibit}</td>
                    <td>
                        <button class="editButton" data-id="${animal.id}">Move</button>
                        <button class="removeButton">Remove</button>
                    </td>
                </tr>
                `)
            }
            else if ( animal.on_display === false ){
                elTwo.append(`
                <tr data-id=${animal.id}>
                    <td>${animal.id}</td>
                    <td>${animal.species}</td>
                    <td>${animal.age}</td>
                    <td>${animal.gender}</td>
                    <td>${animal.name}</td>
                    <td>${animal.exhibit}</td>
                    <td>
                        <button class="editButton" data-id="${animal.id}">Move</button>
                        <button class="removeButton">Remove</button>
                    </td>
                </tr>
                `)
            }
        }//end status marked true (task complete)
    }).catch( function( err ){
            console.log( err );
            alert( 'error in getAnimals', err );
    })//end ajax
}//end getAnimals

function removeAnimal(){
    console.log( 'in deleteAnimal for DELETE' );
    //set variable for unique click
    const myId = $( this ).closest( 'tr' ).data( 'id' )
    //set up ajax for DELETE handshake
    $.ajax({
        method: 'DELETE',
        url: '/api/animals/' + myId
    }).then( function( response ){
        console.log( 'back from server with DELETE', response);
        getAnimals();
    }).catch( function( err ){
        console.log( err );
        alert( 'Error in removeAnimal', err );
    })//end ajax
}

function editAnimal(){
    const myId = $( this ).data( 'id' );
    console.log('in editAnimal w/', myId, $(this), $(this).data );
    //send variable to server/db w/ajax PUT
    $.ajax({
        method: 'PUT',
        url: '/api/animals/' + myId,
    }).then( function( response ){
        console.log( 'back from server with PUT', response );
        getAnimals();
    }).catch( function( err ){
        console.log( err );
        alert( 'Error in editAnimal', err );
    })//end ajax
}//end checkOffTask