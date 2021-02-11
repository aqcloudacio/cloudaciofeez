export default {
  methods: {
    $withoutWatchers (cb) {
      const watchers = this._watchers.map((watcher) => ({ cb: watcher.cb, sync: watcher.sync }))

      for (let index in this._watchers) {
        this._watchers[index] = Object.assign(this._watchers[index], { cb: () => null, sync: true })
      }

      cb()

      for (let index in this._watchers) {
        this._watchers[index] = Object.assign(this._watchers[index], watchers[index])
      }
    }
  }
}
