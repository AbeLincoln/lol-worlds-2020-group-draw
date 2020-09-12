class Team:
    name = ""
    pool = 3
    region = None

    def __init__(self, name, pool, region):
        """

        :param name:
        :param pool:
        :param region:
        """
        self.name = name
        self.pool = pool
        self.region = region

    def __repr__(self):
        return self.name


# major regions:
tes = Team("TES", 1, "China")
jdg = Team("JDG", 2, "China")
sn =  Team("SN",  2, "China")
lgd = Team("LGD", 4, "China")
g2 =  Team("G2",  1, "Europe")
fnc = Team("FNC", 2, "Europe")
rge = Team("RGE", 3, "Europe")
mad = Team("MAD", 4, "Europe")
dwg = Team("DWG", 1, "Korea")
drx = Team("DRX", 2, "Korea")
gen = Team("GEN", 3, "Korea")
tsm = Team("TSM", 1, "North America")
fly = Team("FLY", 3, "North America")
tl =  Team("TL",  4, "North America")
mcx = Team("MCX", 3, "Pacific")
psg = Team("PSG", 4, "Pacific")
# minor regions
itz = Team("ITZ", 4, "Brazil")
uol = Team("UOL", 4, "Russia")
v3 =  Team("V3",  4, "Japan")
r7 =  Team("R7",  4, "Latin America")
lgc = Team("LGC", 4, "Oceania")
sup = Team("SUP", 4, "Turkey")

# assume no upsets
pool1 = [tes, g2, dwg, tsm]
pool2 = [jdg, sn, fnc, drx]
pool3 = [rge, gen, fly, mcx]
pool4 = [lgd, mad, tl, psg]

# dummy pool for the algorithm to leave room open for all regions which COULD advance via Play-Ins and create conflicts
# this pool is the theoretically most difficult set of Play-In winners to be placed into the Main Stage Groups
pool_dummy = [Team("CN", 4, "China"),
              Team("EU", 4, "Europe"),
              Team("NA", 4, "North America"),
              Team("PCS", 4, "Pacific")
              # Team("BR", 4, "Brazil"), #NOTE: Because minor regions can't invalidate the group, they are ignored here
              # Team("CIS", 4, "Russia"),
              # Team("JP", 4, "Japan"),
              # Team("LAT", 4, "Latin America"),
              # Team("OCE", 4, "Oceania"),
              # Team("TR", 4, "Turkey")
              ]
