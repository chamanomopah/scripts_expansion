# 🎯 The Complete Git Worktree + Claude Code Workflow

---

## **📋 Pre-Flight Checklist**

```
# 1 — Start from a clean, up-to-date main
git checkout main
git pull origin main
git status          # → "nothing to commit, working tree clean"

# 2 — Confirm no extra worktrees are already attached
git worktree list   # Should list only your main directory

# 3 — Create a container directory for all worktrees (idempotent)
[ -d WorkTree ] || mkdir WorkTree     # or:  mkdir -p WorkTree
```

---

## **🚀 The Core Parallel-Dev Workflow**

### **1️⃣ Plan Your Features**

| **Why plan?** | **Checklist** |
| --- | --- |
| Avoid merge hell | ▢ Features are **independent** (no file overlap) |
| Reduce context switching | ▢ Each branch has a short, descriptive name |
| Automation & CI clarity | ▢ Naming convention chosen (feature/, fix/, docs/, …) |

---

### **2️⃣ Project Structure**

```
my-project/
├── src/
├── package.json
├── WorkTree/          ← umbrella for all worktrees
└── …other files
```

```
mkdir -p WorkTree      # run once
```

---

### **3️⃣ Create Worktrees (safe syntax)**

```
# git worktree add <path> -B <branch> [<start-point>]
git worktree add -B feature/chat-interface-mem0   WorkTree/chat-ui          # new branch
git worktree add -B feature/mem0-integration-tests WorkTree/mem0-tests      # new branch

git worktree list -v
```

Example output:

```
/path/to/project                       [main]
/path/to/project/WorkTree/chat-ui      [feature/chat-interface-mem0]
/path/to/project/WorkTree/mem0-tests   [feature/mem0-integration-tests]
```

> Tip:
> 

> Lock the primary worktree to prevent accidental deletion:
> 

> git worktree lock .
> 

---

### **4️⃣ Launch Claude Code Instances**

```
# Terminal 1
cd WorkTree/chat-ui
claude --dangerously-skip-permissions
claude for safe mode
# Terminal 2
cd WorkTree/mem0-tests
claude --dangerously-skip-permissions
claude for safe mode

```

(Optional) Seed each worktree with a tiny context file:

```
echo "ROLE: You are working only on Chat UI. Ignore backend files." \
     > .claude-context
```

Claude Code auto-prepends the file to every prompt.

---

### **5️⃣ Give Claude Clear Context**

- **Goal:** “Build Chat UI with mem0 memory layer.”
- **Files to edit:** src/components/Chat/**
- **Constraints:** Do **not** touch server code.
- **Done-when:** Cypress tests pass.

---

### **6️⃣ Monitor Progress**

- Run **tmux** / **screen** so sessions survive disconnects.
- Enable terminal bells or OS notifications for when Claude pauses.
- Keep an eye on **Anthropic token usage** if you parallelize aggressively.

---

### **7️⃣ Test Each Feature in Isolation**

```
# Worktree A
cd WorkTree/chat-ui
pnpm test && pnpm run dev

# Worktree B
cd WorkTree/mem0-tests
pnpm test
```

---

### **8️⃣ Create PR → Merge → Clean Up**

```
# ① Push feature branch
cd WorkTree/chat-ui
git push -u origin feature/chat-interface-mem0

# ② Open PR (GitHub CLI)
gh pr create --title "Chat UI w/ mem0" \
             --body  "Implements chat interface using mem0 memory layer." \
             --base main --head feature/chat-interface-mem0

# ③ After PR is merged on GitHub…
cd ../..          # project root
git checkout main
git pull origin main

# ④ Remove local resources
git worktree remove WorkTree/chat-ui
git branch -D feature/chat-interface-mem0
git worktree prune          # scrub dangling refs
```

Repeat for each worktree.

---

## **📊 Scaling to 3-Plus Parallel Streams**

```
git worktree add -B feature/chat-interface   WorkTree/chat-ui
git worktree add -B feature/authentication   WorkTree/auth-system
git worktree add -B fix/playwright-tests     WorkTree/test-suite
git worktree add -B docs/api-documentation   WorkTree/docs-update
```

### **Naming Conventions**

| **Branch prefix** | **Use for** |
| --- | --- |
| feature/ | New features |
| fix/ | Bug fixes |
| refactor/ | Code restructuring |
| docs/ | Documentation |
| test/ | Test additions |

Worktree directories mirror the branch but stay short, e.g.:

```
WorkTree/chat-ui
WorkTree/auth-system
```

---

## **🛠️ Helpful Shell Aliases**

```
# ~/.zshrc or ~/.bashrc

# List worktrees verbosely
alias wt='git worktree list -v'

# Add a worktree: wtadd <dir> <branch>
wtadd () {
  local dir=$1; local br=$2
  [ -z "$dir" ] && echo "dir missing" && return
  [ -z "$br"  ] && echo "branch missing" && return
  git worktree add -B "$br" "WorkTree/$dir"
}

# Remove & delete branch: wtrm <dir> <branch>
wtrm () {
  git worktree remove --force "WorkTree/$1" && git branch -D "$2"
  git worktree prune
}

# Quick cd helpers
alias wtcd='cd WorkTree'
alias wtls='ls -la WorkTree'
wtgo () { cd "WorkTree/$1"; }
```

---

## **🚨 Common Scenarios**

| **Situation** | **Command / Fix** |
| --- | --- |
| **Need shared changes** | Create a base/shared-updates branch first, branch features from there. |
| **Claude finished but manual tweaks needed** | Edit in the worktree ➜ git commit -m "Manual fixes" |
| **Compare all branches quickly** | git log --all --oneline --graph -20 |
| **Nuke all worktrees** | git worktree list --porcelain | awk '/worktree/ {print $2}' | xargs -n1 git worktree remove --force && git worktree prune |

---

## **📈 Pro Tips**

1. **Disk usage:** Node modules multiply. Use pnpm’s shared store (pnpm config set shared-workspace-lockfile true) or mount node_modules via symlinks.
2. **CI builds:** Ensure your CI fetches full history (fetch-depth: 0) so detached worktree commits aren’t lost.
3. **Performance:** Limit each Claude with --max-tokens-per-minute if you hit Anthropic rate caps.
4. **IDE colour-coding:** Many editors let you set window tint per-folder—helps avoid “which worktree am I in?” mistakes.

---

## **🎓 First-Run Checklist**

- Main branch clean & pulled
- WorkTree/ exists
- Worktrees created with -B
- Claude running in each worktree
- Clear instructions supplied to each agent
- Tests passing independently
- PR merged via GitHub
- git worktree prune + local branch deletion complete

---

## **💡 End-to-End Example (2 Features)**

```
git checkout main && git pull
mkdir -p WorkTree

git worktree add -B feature/chat-ui          WorkTree/chat-ui
git worktree add -B feature/mem0-tests       WorkTree/mem0-tests

# === two shells open, run `claude` in each ===

# When chat-ui done
cd WorkTree/chat-ui
git push -u origin feature/chat-ui
# (merge PR on GitHub)
cd ../..
git checkout main && git pull
git worktree remove WorkTree/chat-ui && git branch -D feature/chat-ui
git worktree prune

# Repeat for mem0-tests …

# Remove umbrella dir if empty
rmdir WorkTree
```

---

## **✅ When to Use This Technique**

| **Perfect for** | **Avoid if** |
| --- | --- |
| Independent features | Heavy overlap on same files |
| Parallel bug-fixes | Sequential tasks or tiny edits |
| Separate test suites | You only need **one** quick branch |

**Consistency** in naming + cleanup is the secret sauce. Follow the checklist, and your parallel Claude Code swarm will hum without a hitch.

Happy hacking, Sami—Jarvis out. 🛡️