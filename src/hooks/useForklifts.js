import { useEffect, useState } from 'react'

// 1. Targonca lista lekérése a megadott táblák (teszt1-6) alapján
export function useForklifts() {
  const [forklifts, setForklifts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    const list = [
      { id: 1, name: 'Targonca 1' },
      { id: 2, name: 'Targonca 2' },
      { id: 3, name: 'Targonca 3' },
      { id: 4, name: 'Targonca 4' },
      { id: 5, name: 'Targonca 5' },
      { id: 6, name: 'Targonca 6' },
    ]
    setForklifts(list)
  }, [])

  return { forklifts, error }
}

export function useForkliftDays(forkliftId) {
  const [days, setDays] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!forkliftId) {
      setDays([])
      return
    }
    setDays([]) 
  }, [forkliftId])

  return { days, loading, error }
}

export function useForkliftPositions(forkliftId, date, startTime = '00:00:00', endTime = '23:59:59') {
  const [points, setPoints] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!forkliftId || !date) {
      setPoints([])
      return
    }

    setLoading(true)
    fetch(`/api/positions?forklift_id=${forkliftId}&date=${date}&start_time=${startTime}&end_time=${endTime}`)
      .then((res) => {
        if (!res.ok) throw new Error('Hiba a pozíciók lekérésekor')
        return res.json()
      })
      .then((rows) => {
        setPoints(rows || [])
        setError(null)
      })
      .catch(() => setError('Nem sikerült betölteni a pozíciókat.'))
      .finally(() => setLoading(false))
  }, [forkliftId, date, startTime, endTime])

  return { 
    count: points.length, 
    distance_m: 0, 
    points, 
    loading, 
    error 
  }
}