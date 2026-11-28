"""Per-trade content for homepage mockups. Copy is generic-but-specific so it's true for any business of that trade."""
F = {  # family palettes: bg, ink, accent, soft
 "dark":  ("#0f0f10", "#f4f1ea", "#c8a96a", "#1b1b1d"),
 "warm":  ("#fbf7f1", "#1e1a16", "#b4532a", "#f1e8dc"),
 "fresh": ("#f6f8f7", "#14201c", "#1f7a5a", "#e4eee9"),
 "navy":  ("#f5f7fa", "#0f1b2d", "#e0562b", "#e7edf5"),
 "blush": ("#fbf6f4", "#2a1d1d", "#b35d6b", "#f3e6e3"),
}
T = {
 "barber": ("dark", "Sharp cuts. No waiting around.", ["Skin fades", "Scissor cuts", "Beard trims & shapes", "Hot towel shaves", "Kids' cuts"], "a moody modern barbershop interior, leather barber chair, warm tungsten light, no people, photo"),
 "dog groomer": ("fresh", "Happy dogs, fresh coats, calm grooming.", ["Full groom", "Bath & tidy", "Puppy introduction", "Nail clipping", "De-shedding"], "a freshly groomed fluffy cockapoo sitting on a grooming table in a bright clean salon, photo"),
 "car valeting": ("dark", "Showroom finish, at your door.", ["Mini valet", "Full valet", "Interior deep clean", "Machine polish", "Ceramic coating"], "a glossy black car being hand-polished, water beading on the bonnet, dramatic light, photo"),
 "dog walker": ("fresh", "Trusted walks while you're at work.", ["Solo walks", "Group walks", "Puppy visits", "Home pet sitting", "Weekend cover"], "a happy dog on a lead walking through an English park in autumn, photo"),
 "massage therapist": ("warm", "Ease the tension. Book in minutes.", ["Deep tissue", "Sports massage", "Swedish massage", "Pregnancy massage", "Hot stones"], "a calm massage treatment room with warm low light, folded towels and a plant, no people, photo"),
 "nail salon": ("blush", "Nails that last. Appointments that run on time.", ["Gel manicure", "BIAB", "Acrylic sets", "Pedicures", "Nail art"], "elegant manicured nails in a soft neutral colour resting on a marble table, photo"),
 "beauty salon": ("blush", "Look after yourself. We'll do the rest.", ["Brows & lashes", "Facials", "Waxing", "Spray tans", "Make-up"], "a bright elegant beauty salon treatment room, soft daylight, no people, photo"),
 "driving instructor": ("navy", "Pass with confidence, first time.", ["Beginner lessons", "Intensive courses", "Test preparation", "Motorway lessons", "Refresher lessons"], "a modern hatchback learner car with L plates parked on a quiet British street, photo"),
 "personal trainer": ("dark", "Real results. A plan built around you.", ["1-to-1 training", "Weight loss", "Strength & conditioning", "Nutrition coaching", "Online coaching"], "a clean private gym with dumbbells and a squat rack, dramatic light, no people, photo"),
 "tattoo studio": ("dark", "Custom work, done properly.", ["Custom designs", "Fine line", "Blackwork", "Cover-ups", "Consultations"], "a clean modern tattoo studio interior, black walls, warm lamps, no people, photo"),
 "plasterer": ("navy", "Smooth walls. Tidy job. Fair price.", ["Skimming", "Re-plastering", "Rendering", "Ceiling repairs", "Coving"], "a freshly skimmed smooth plaster wall in a bright empty room, photo"),
 "joiner": ("warm", "Quality joinery, built to last.", ["Doors & frames", "Fitted wardrobes", "Staircases", "Skirting & architrave", "Kitchens"], "a beautifully crafted oak staircase in a modern British home, photo"),
 "electrician": ("navy", "Safe, certified, on time.", ["Rewires", "Consumer units", "EV chargers", "Fault finding", "EICR certificates"], "a neat modern consumer unit and tidy wiring in a bright room, photo"),
 "painter and decorator": ("warm", "A finish you'll notice every day.", ["Interior painting", "Exterior painting", "Wallpapering", "Woodwork", "Commercial"], "a freshly painted modern living room in a warm sage colour, photo"),
 "photographer": ("dark", "Photos you'll actually want on the wall.", ["Portraits", "Families", "Events", "Headshots", "Products"], "a professional camera on a wooden table with soft window light, photo"),
 "cafe": ("warm", "Good coffee, proper food, friendly faces.", ["Breakfast", "Lunch", "Cakes & bakes", "Takeaway coffee", "Private hire"], "a cosy independent cafe counter with cakes and a coffee machine, warm light, photo"),
 "boiler engineer": ("navy", "Warm home, fixed fast.", ["Boiler repairs", "New boiler installs", "Annual servicing", "Gas safety certificates", "Power flushing"], "a modern white combi boiler neatly installed in a kitchen cupboard, photo"),
 "plumber": ("navy", "Leaks fixed. Jobs done right.", ["Emergency call-outs", "Bathrooms", "Leaks & repairs", "Taps & toilets", "Radiators"], "a modern bathroom with chrome taps and a walk-in shower, photo"),
 "roofer": ("navy", "Watertight roofs, honest quotes.", ["Roof repairs", "New roofs", "Flat roofs", "Guttering", "Chimney work"], "a new slate roof on a British house against a blue sky, photo"),
 "landscaper": ("fresh", "Gardens you'll want to spend time in.", ["Patios", "Fencing", "Turfing", "Planting", "Garden design"], "a newly landscaped British garden with a stone patio and fresh lawn, photo"),
 "hairdresser": ("blush", "Hair you'll love, every visit.", ["Cut & finish", "Colour", "Balayage", "Blow-dries", "Treatments"], "a bright stylish hair salon with mirrors and chairs, no people, photo"),
 "window cleaner": ("fresh", "Sparkling windows, reliable rounds.", ["Windows", "Frames & sills", "Conservatories", "Gutter clearing", "Commercial"], "sparkling clean windows on a British terraced house in sunshine, photo"),
 "builder": ("navy", "Extensions and renovations, done right.", ["Extensions", "Loft conversions", "Renovations", "Brickwork", "Groundworks"], "a finished modern single-storey house extension with bifold doors, photo"),
 "bakery": ("warm", "Baked fresh every morning.", ["Bread", "Cakes", "Pastries", "Celebration cakes", "Wholesale"], "fresh sourdough loaves and pastries on a rustic bakery counter, photo"),
 "removals": ("navy", "Stress-free moves, handled with care.", ["House moves", "Office moves", "Packing", "Storage", "Man & van"], "a clean removals van with neatly stacked boxes, photo"),
 "aesthetics clinic": ("blush", "Natural results, expert care.", ["Skin treatments", "Lip filler", "Skin boosters", "Chemical peels", "Consultations"], "a calm bright aesthetics clinic treatment room, no people, photo"),
 "mobile mechanic": ("dark", "We come to you. Fixed on the driveway.", ["Servicing", "Brakes", "Diagnostics", "Clutches", "Pre-MOT checks"], "a mechanic's tools laid out beside a car wheel on a driveway, photo"),
 "gardener": ("fresh", "Tidy gardens, all year round.", ["Lawn mowing", "Hedge trimming", "Garden clearance", "Weeding", "Seasonal tidy"], "a neatly mown striped lawn and trimmed hedges in an English garden, photo"),
 "handyman": ("navy", "No job too small. Done properly.", ["Flat-pack assembly", "Shelves & TVs", "Small repairs", "Doors & locks", "Odd jobs"], "a tidy toolbox and drill on a wooden floor in a bright home, photo"),
 "florist": ("blush", "Flowers for every moment.", ["Bouquets", "Weddings", "Funerals", "Events", "Same-day delivery"], "a beautiful seasonal bouquet of flowers on a wooden counter, photo"),
}
DEFAULT = ("navy", "Local, reliable and easy to book.", ["Our services", "Free quotes", "Fully insured", "Local and reliable", "Fast response"], "a bright modern British high street shopfront, photo")

def get(trade):
    t = T.get((trade or "").lower(), DEFAULT)
    return {"family": t[0], "palette": F[t[0]], "tagline": t[1], "services": t[2], "hero_prompt": t[3]}
