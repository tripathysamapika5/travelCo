var survey_options = document.getElementById('survey_options');
var add_more_fields = document.getElementById('add_more_fields');
var remove_fields = document.getElementById('remove_fields');

add_more_fields.onclick = function(){
  var newField = document.createElement('select');
  newField.setAttribute('type','text');
  newField.setAttribute('name','survey_options[]');
  newField.setAttribute('class','custom-select');
  newField.setAttribute('siz',50);
  newField.setAttribute('placeholder','Gender');
  var OPT0 = document.createElement('OPTION');
OPT0.setAttribute('value', 0);
  var OPT1 = document.createElement('OPTION');
OPT1.setAttribute('value', 0);
var OPT2 = document.createElement('OPTION');
OPT2.setAttribute('value', 0);
var OPT3 = document.createElement('OPTION');
OPT3.setAttribute('value', 0);
OPT0.selected = true

  OPT0.appendChild( document.createTextNode( 'Gender' ) );
  OPT1.appendChild( document.createTextNode( 'Male' ) );
OPT2.appendChild( document.createTextNode( 'Female' ) );
OPT3.appendChild( document.createTextNode( 'Any' ) );

newField.appendChild(OPT0);
newField.appendChild(OPT1);
newField.appendChild(OPT2);
newField.appendChild(OPT3);
survey_options.appendChild(newField);

  //survey_options.appendChild(newField);
  var newField2 = document.createElement('select');

  var OPTN0 = document.createElement('OPTION');
OPTN0.setAttribute('value', 0);
  var OPTN1 = document.createElement('OPTION');
OPTN1.setAttribute('value', 0);
var OPTN2 = document.createElement('OPTION');
OPTN2.setAttribute('value', 0);
var OPTN3 = document.createElement('OPTION');
OPTN3.setAttribute('value', 0);
 var OPTN4 = document.createElement('OPTION');
OPTN4.setAttribute('value', 0);
  var OPTN5 = document.createElement('OPTION');
OPTN5.setAttribute('value', 0);
var OPTN6 = document.createElement('OPTION');
OPTN6.setAttribute('value', 0);
var OPTN7 = document.createElement('OPTION');
OPTN7.setAttribute('value', 0);
 var OPTN8 = document.createElement('OPTION');
OPTN8.setAttribute('value', 0);
  var OPTN9 = document.createElement('OPTION');
OPTN9.setAttribute('value', 0);
var OPTN10 = document.createElement('OPTION');
OPTN10.setAttribute('value', 0);
var OPTN11 = document.createElement('OPTION');
OPTN11.setAttribute('value', 0);
 var OPTN12 = document.createElement('OPTION');
OPTN12.setAttribute('value', 0);
  var OPTN13 = document.createElement('OPTION');
OPTN13.setAttribute('value', 0);
var OPTN14 = document.createElement('OPTION');
OPTN14.setAttribute('value', 0);
var OPTN15 = document.createElement('OPTION');
OPTN15.setAttribute('value', 0);
 var OPTN16 = document.createElement('OPTION');
OPTN16.setAttribute('value', 0);
  var OPTN17 = document.createElement('OPTION');
OPTN17.setAttribute('value', 0);
 var OPTN18 = document.createElement('OPTION');
OPTN18.setAttribute('value', 0);
OPTN0.selected = true

  OPTN0.appendChild( document.createTextNode( 'Age Group' ) );
  OPTN1.appendChild( document.createTextNode( '0-5' ) );
OPTN2.appendChild( document.createTextNode( '6-10' ) );
OPTN3.appendChild( document.createTextNode( '11-15' ) );
OPTN4.appendChild( document.createTextNode( '16-20' ) );
OPTN5.appendChild( document.createTextNode( '21-25' ) );
OPTN6.appendChild( document.createTextNode( '26-30' ) );
OPTN7.appendChild( document.createTextNode( '31-35' ) );
OPTN8.appendChild( document.createTextNode( '36-40' ) );
OPTN9.appendChild( document.createTextNode( '41-45' ) );
OPTN10.appendChild( document.createTextNode( '46-50' ) );
OPTN11.appendChild( document.createTextNode( '51-55' ) );
OPTN12.appendChild( document.createTextNode( '56-60' ) );
OPTN13.appendChild( document.createTextNode( '61-65' ) );
OPTN14.appendChild( document.createTextNode( '66-70' ) );
OPTN15.appendChild( document.createTextNode( '71-75' ) );
OPTN16.appendChild( document.createTextNode( '76-80' ) );
OPTN17.appendChild( document.createTextNode( '81-85' ) );
OPTN18.appendChild( document.createTextNode( '85+' ) );

  newField2.setAttribute('type','text');
  newField2.setAttribute('name','survey_options[]');
  newField2.setAttribute('class','custom-select');
  newField2.setAttribute('siz',50);
  newField2.setAttribute('placeholder','Age Group');

  newField2.appendChild(OPTN0);
newField2.appendChild(OPTN1);
newField2.appendChild(OPTN2);
newField2.appendChild(OPTN3);
newField2.appendChild(OPTN4);
newField2.appendChild(OPTN5);
newField2.appendChild(OPTN6);
newField2.appendChild(OPTN7);
newField2.appendChild(OPTN8);
newField2.appendChild(OPTN9);
newField2.appendChild(OPTN10);
newField2.appendChild(OPTN11);
newField2.appendChild(OPTN12);
newField2.appendChild(OPTN13);
newField2.appendChild(OPTN14);
newField2.appendChild(OPTN15);
newField2.appendChild(OPTN16);
newField2.appendChild(OPTN17);
newField2.appendChild(OPTN18);
survey_options.appendChild(newField2);

var newField3 = document.createElement('select');
  newField3.setAttribute('type','text');
  newField3.setAttribute('name','survey_options[]');
  newField3.setAttribute('class','custom-select');
  newField3.setAttribute('siz',50);
  newField3.setAttribute('placeholder','Vacinated');

  var OPTNS0 = document.createElement('OPTION');
OPTNS0.setAttribute('value', 0);
  var OPTNS1 = document.createElement('OPTION');
OPTNS1.setAttribute('value', 0);
var OPTNS2 = document.createElement('OPTION');
OPTNS2.setAttribute('value', 0);

OPTNS0.selected = true

  OPTNS0.appendChild( document.createTextNode( 'Vaccination Status' ) );
  OPTNS1.appendChild( document.createTextNode( 'Yes' ) );
OPTNS2.appendChild( document.createTextNode( 'No' ) );


newField3.appendChild(OPTNS0);
newField3.appendChild(OPTNS1);
newField3.appendChild(OPTNS2);

survey_options.appendChild(newField3);

}

remove_fields.onclick = function(){
  var input_tags = survey_options.getElementsByTagName('select');
  if(input_tags.length > 3) {
    survey_options.removeChild(input_tags[(input_tags.length) - 1]);
    survey_options.removeChild(input_tags[(input_tags.length) - 1]);
    survey_options.removeChild(input_tags[(input_tags.length) - 1]);
  }
}
