var W = 200;
var H = 200;

function setup() {
    createCanvas(W,H);
    angleMode(DEGREES);
  }
 
function draw() {
    //background(0);
    clear();
    translate(W/2, H/2);
    rotate(-90);
 
    var hr = hour();
    var mn = minute();
    var sc = second();
 
    strokeWeight(8);
    stroke(255, 100, 150);
    noFill();
    var secondAngle = map(sc, 0, 60, 0, 360);
    arc(0, 0, H*0.75, H*0.75, 0, secondAngle);
 
    stroke(255,0,0);
    var minuteAngle = map(mn, 0, 60, 0, 360);
    arc(0, 0, H/2 +20, H/2 + 20, 0, minuteAngle);
 
    stroke(150, 255, 100);
    var hourAngle = map(hr % 12, 0, 12, 0, 360);
    arc(0, 0, H/2 -10, H/2 - 10, 0, hourAngle);
 
    push();
    rotate(secondAngle);
    stroke(255, 100, 150);
    line(0, 0, H/4, 0);
    pop();
 
    push();
    rotate(minuteAngle);
    stroke(255, 0, 0);
    line(0, 0, H/5, 0);
    pop();
 
    push();
    rotate(hourAngle);
    stroke(150, 255, 100);
    line(0, 0, H/8, 0);
    pop();
 
    stroke(255);
    point(0, 0);
    //redraw();
  }