resizeBackground();

var FROG = {
  green: {
    color: 'green',
    img: 'imgs/frogGreen.png'
  },
  red: {
    color: 'red',
    img: 'imgs/frogRed.png'
  }
};

var BLANK_SPACE = "blank";
var START_ARRAY = [];
var FINAL_ARRAY = [];

var posArray = [];
var prevArray = [];
var counter = 0;
var move = "N/A";

window.onresize = function() {
    resizeBackground();
}

setFrogNum($('#frogNumberSelector').children('option:selected').val());

function setFrogNum(num) {
  var columns = Number((num * 2) + 1);
  $('.frog').remove();
  counter = 0;
  buildArrays(num);
  prevArray = [];
  posArray = [];
  prevArray.push(START_ARRAY.slice());
  posArray = START_ARRAY.slice();
  buildFrogs();
  $('.frogGrid').css('grid-template-columns', 'repeat(' + columns + ', 1fr)');
  displayFrogs();
  resizeBackground();
  addToTable();
  emptyTable();
}

function buildArrays(num) {
  START_ARRAY = [BLANK_SPACE];
  FINAL_ARRAY = [BLANK_SPACE];
  for (var i = 0; i < num; i++) {
    START_ARRAY.unshift(FROG.red.color);
    START_ARRAY.push(FROG.green.color);
    FINAL_ARRAY.unshift(FROG.green.color);
    FINAL_ARRAY.push(FROG.red.color);
  }
}

function buildFrogs() {
  var list = document.getElementById('frogList');
  for (var i = 0; i < START_ARRAY.length; i++) {
    var listItem = document.createElement('li');
    listItem.setAttribute('id', 'pos' + i);
    listItem.setAttribute('class', 'frog');
    document.getElementById('frogList').appendChild(listItem);

  }
}

function displayFrogs() {
  $('#counter').html(counter);
  for (var i = 0; i < posArray.length; i++) {
    if (posArray[i] == FROG.red.color) {
      $('#pos' + i).html('<img class="clickable" src="' + FROG.red.img + '" alt="red frog" >');
    } else if (posArray[i] == FROG.green.color) {
      $('#pos' + i).html('<img class="clickable" src="' + FROG.green.img + '" alt="green frog" >');
    } else {
      $('#pos' + i).html('<img src="imgs/blankSpace.png" alt="" >');
    }
  }
}

function addToTable() {
  var table = document.getElementById('moveTable');
  var tableRow = document.createElement('tr');
  var stepNum = document.createElement('td');
  var posStr = '';
  var curPos = document.createElement('td');
  var moveMade = document.createElement('td');
  stepNum.textContent = counter;
  for (var i = 0; i < posArray.length; ++i) {
    switch (posArray[i]) {
      case FROG.red.color:
        posStr += 'R '; break;
      case FROG.green.color:
        posStr += 'G '; break;
      default:
        posStr += 'S '
    }
  }
  curPos.textContent = posStr;
  moveMade.textContent = move;
  tableRow.appendChild(stepNum);
  tableRow.appendChild(curPos);
  tableRow.appendChild(moveMade);
  table.appendChild(tableRow);
}

function makeMove(index) {
  if (!compareArrays(prevArray[prevArray.length - 1], posArray))
    prevArray.push(posArray.slice());
  switch (posArray[index]) {
    case FROG.red.color:
      if (posArray[index + 1] == BLANK_SPACE) {
        posArray[index + 1] = FROG.red.color;
        posArray[index] = BLANK_SPACE;
        move = "Shift Right";
        counter++;
        addToTable();
      } else if (posArray[index + 2] == BLANK_SPACE) {
        posArray[index + 2] = FROG.red.color;
        posArray[index] = BLANK_SPACE;
        move = "Jump Right";
        counter++;
        addToTable();
      }
      break;
    case FROG.green.color:
      if (posArray[index - 1] == BLANK_SPACE) {
        posArray[index - 1] = FROG.green.color;
        posArray[index] = BLANK_SPACE;
        move = "Shift Left";
        counter++;
        addToTable();
      } else if (posArray[index - 2] == BLANK_SPACE) {
        posArray[index - 2] = FROG.green.color;
        posArray[index] = BLANK_SPACE;
        move = "Jump Left";
        counter++;
        addToTable();
      }
      break;
  };
  displayFrogs();
  if (compareArrays(posArray, FINAL_ARRAY)) {
    alert('Congratulations, you did it!');
  }
}

function resetFrogs() {
  posArray = START_ARRAY.slice();
  prevArray = [];
  prevArray.push(START_ARRAY.slice());
  counter = 0;
  displayFrogs();
  emptyTable();
}

function compareArrays(x, y) {
  if (x.length != y.length)
    return false;
  for (var i = 0; i < x.length; i++) {
    if (x[i] != y[i])
      return false;
  }
  return true;
}

function undo() {
  if (prevArray[prevArray.length - 1] != null) {
    if (compareArrays(prevArray[prevArray.length - 1], posArray) && prevArray.length > 1) {
      prevArray.pop();
    }
    posArray = prevArray[prevArray.length - 1].slice();
    if (prevArray.length > 1) {
      prevArray.pop();
    }
  }
  if (!compareArrays(prevArray, posArray) && counter > 0)
    counter--;
  displayFrogs();
  var tableRow = document.getElementById('moveTable').rows.length;
  if (tableRow > 2) {
    document.getElementById('moveTable').deleteRow(tableRow - 1);
  }
}

function emptyTable() {
  var table = document.getElementById('moveTable');
  while (table.rows.length > 2) {
    table.deleteRow(2);
  }
}

function resizeBackground() {
    $('.mainGrid').width($('.mainGrid').closest('.rendered_html').width());
    $('.mainGrid').height($('.mainGrid').closest('.rendered_html').width() * 0.53);
}

$('#frogNumberSelector').change(function() {
  setFrogNum($(this).children('option:selected').val());
});

$(document).on('click', '.frog', function() {
  var pos = $(this).index();
  // - 3 since the index of the list already has 3 elements for the buttons
  makeMove(pos - 3);
});
