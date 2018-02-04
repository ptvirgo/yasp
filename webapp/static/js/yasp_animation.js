$(document).ready(function() {

    s = Snap("#comic");
    Snap.load("/static/style/yasp.svg", function(f) {
        s.add(f.select("*"));

        var kid = s.select("#kid");
        var kid_shirt = s.select("#shirt");
        var kid_pants = s.select("#pants");
        var door = s.select("#door");

        var kid_body = s.select("#kid_body");
        kid_body.attr({fill: randomSkin()});
        var prisoner_body = s.select("#prisoner_body");
        prisoner_body.attr({fill: randomSkin()});
        var guard_body = s.select("#guard_body");
        guard_body.attr({fill: randomSkin()});

        door.open = function(c) {
            door.animate({transform: 't100,0' }, 2000, c);
        };
        door.close = function(c) {
            door.animate({transform: 't0,0' }, 750, mina.bounce, c);
        };

        kid.move = function(c) {
            kid.animate({transform: 't125,-75'}, 500, c);
        }        

        kid.change = function() {
            kid_shirt.animate({fill: "rgba(255,102,0,255)"}, 1000)
            kid_pants.animate({fill: "rgba(255,102,0,255)"}, 1000)
        };

        door.open( function() { kid.move( function() { door.close( kid.change)})})

    });

});

function randomSkin() {
    var skintones = ["#2B1100", "#803300", "#DEAA87",
                     "#C8BEB7", "#C87137", "#F4D7D7"];
    tone = skintones[Math.floor(Math.random() * skintones.length)];
    return tone;
}
