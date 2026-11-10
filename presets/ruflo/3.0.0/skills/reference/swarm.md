# Swarm Commands

## init — Initialize a swarm

```bash
ucli ruflo swarm init
ucli ruflo swarm init --topology hierarchical --max-agents 10 --strategy specialized
```

Also supports: `--topology`, `--max-agents`, `--strategy`, `--config`
(topologies: hierarchical, mesh, hierarchical-mesh, ring, star, hybrid, adaptive)
(strategies: specialized, balanced, adaptive)

## status — Get swarm status

```bash
ucli ruflo swarm status
ucli ruflo swarm status --swarm-id swarm-1
```

Also supports: `--swarm-id`

## health — Check swarm health

```bash
ucli ruflo swarm health
ucli ruflo swarm health --swarm-id swarm-1
```

## shutdown — Shutdown a swarm

```bash
ucli ruflo swarm shutdown
ucli ruflo swarm shutdown --swarm-id swarm-1 --graceful false
```

Also supports: `--swarm-id`, `--graceful`

Use `ucli ruflo swarm <action> --help` for full parameter details.
