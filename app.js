const rootMeData = {
    username: "ctrlstack",
    rank: 51689,
    points: 325,
    challengesSolved: 29,
    categories: [
        { name: "Forensic", count: 12, icon: "fa-magnifying-glass" },
        { name: "Cracking", count: 5, icon: "fa-gears" },
        { name: "Web Client", count: 8, icon: "fa-code" },
        { name: "App - Script", count: 4, icon: "fa-scroll" }
    ],
    recentChallenges: [
        "Forensic - Command & Control - Level 1",
        "Forensic - Find my password",
        "Cracking - ELF - x86 Basic",
        "Web Client - Javascript - Authentication"
    ]
};

const fcscData = {
    year: 2025,
    categories: [
        {
            name: "Forensic",
            icon: "fa-magnifying-glass",
            challenges: [
                { id: 1, title: "Analyse mémoire 1/5 - Exfiltration", difficulty: "Easy" },
                { id: 2, title: "Analyse mémoire 2/5 - Origine de la menace", difficulty: "Medium" },
                { id: 3, title: "Analyse mémoire 3/5 - Où est le pansement ?", difficulty: "Medium" },
                { id: 4, title: "Analyse mémoire 4/5 - Un échelon de plus dans la chaîne", difficulty: "Hard" },
                { id: 5, title: "Analyse mémoire 5/5 - Le commencement", difficulty: "Hard" }
            ]
        },
        {
            name: "Intro / Simple",
            icon: "fa-star",
            challenges: [
                { id: 101, title: "Analyse mémoire - Pour commencer (1/2)", difficulty: "Intro" },
                { id: 102, title: "Analyse mémoire - Pour commencer (2/2)", difficulty: "Intro" },
                { id: 103, title: "Badd Circuit", difficulty: "Intro" },
                { id: 104, title: "Carotte Radis Tomate", difficulty: "Intro" },
                { id: 105, title: "Catch me if you can", difficulty: "Intro" },
                { id: 106, title: "iForensics - iCrash", difficulty: "Intro" },
                { id: 107, title: "Intro to pwntools", difficulty: "Intro" },
                { id: 108, title: "Sloubi", difficulty: "Intro" },
                { id: 109, title: "Smölkkey", difficulty: "Intro" },
                { id: 110, title: "SOCrate 1/6 - Technologie", difficulty: "Intro" },
                { id: 111, title: "Docker et Netcat", difficulty: "Intro" },
                { id: 112, title: "Cap ou Pcap", difficulty: "Intro" }
            ]
        },
        {
            name: "Web",
            icon: "fa-globe",
            challenges: [
                { id: 201, title: "Meme Generator", difficulty: "Intro" },
                { id: 202, title: "Babel Web", difficulty: "Intro" }
            ]
        }
    ]
};

function renderRootMe() {
    const container = document.getElementById('root-me-content');
    if (!container) return;

    let html = `
        <div class="card p-6 rounded-xl lg:col-span-4 md:col-span-2">
            <div class="flex flex-wrap justify-around text-center gap-6">
                <div>
                    <p class="text-slate-400 text-sm uppercase tracking-wider mb-1">Points</p>
                    <p class="text-4xl font-bold text-sky-400">${rootMeData.points}</p>
                </div>
                <div>
                    <p class="text-slate-400 text-sm uppercase tracking-wider mb-1">Classement</p>
                    <p class="text-4xl font-bold text-indigo-400">#${rootMeData.rank}</p>
                </div>
                <div>
                    <p class="text-slate-400 text-sm uppercase tracking-wider mb-1">Challenges</p>
                    <p class="text-4xl font-bold text-emerald-400">${rootMeData.challengesSolved}</p>
                </div>
            </div>
        </div>
    `;

    rootMeData.categories.forEach(cat => {
        html += `
            <div class="card p-6 rounded-xl flex items-center gap-4">
                <div class="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center text-sky-400 text-xl">
                    <i class="fa-solid ${cat.icon}"></i>
                </div>
                <div>
                    <h3 class="font-bold text-lg">${cat.name}</h3>
                    <p class="text-slate-400">${cat.count} validés</p>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

function renderFCSC() {
    const container = document.getElementById('fcsc-content');
    if (!container) return;

    let html = '';
    fcscData.categories.forEach(cat => {
        html += `
            <div class="col-span-full mt-8 mb-4">
                <h3 class="text-xl font-bold flex items-center gap-2 text-slate-300">
                    <i class="fa-solid ${cat.icon} text-indigo-400"></i>
                    ${cat.name}
                </h3>
            </div>
        `;

        cat.challenges.forEach(chall => {
            const diffColor = chall.difficulty === 'Intro' ? 'text-emerald-400' :
                              chall.difficulty === 'Easy' ? 'text-sky-400' : 
                              chall.difficulty === 'Medium' ? 'text-amber-400' : 'text-rose-400';
            
            html += `
                <div class="card p-5 rounded-xl border-l-2 border-indigo-500/50 hover:border-indigo-400 transition-colors">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 bg-indigo-500/10 text-indigo-300 rounded">${cat.name}</span>
                        <span class="text-[10px] font-bold ${diffColor} uppercase">${chall.difficulty}</span>
                    </div>
                    <h4 class="text-base font-bold mb-3 text-slate-100">${chall.title}</h4>
                    <div class="flex items-center gap-1.5 text-emerald-400 text-xs font-medium">
                        <i class="fa-solid fa-circle-check"></i>
                        <span>Validé</span>
                    </div>
                </div>
            `;
        });
    });

    container.innerHTML = html;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Simulate a small delay for "loading" effect
    setTimeout(() => {
        renderRootMe();
        renderFCSC();
    }, 800);
});
